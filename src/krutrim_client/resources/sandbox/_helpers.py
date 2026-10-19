from __future__ import annotations

import io
import os
import re
from typing import Mapping, Sequence
from pathlib import Path

import anyio

from ...types.sandbox import SandboxFileContent

MAX_BODY_BYTES = 100 * 1024 * 1024
DNS_1035_NAME = re.compile(r"^[a-z]([-a-z0-9]*[a-z0-9])?$")
MAX_SANDBOX_NAME_LEN = 28
MAX_LABELS = 16
MAX_LABEL_KEY_LEN = 63
MAX_LABEL_VALUE_LEN = 255

# The service accepts every network-policy parameter, echoes them back on the
# update path, and enforces none of them: a sandbox created with
# allow_internet_access=False still reaches the public internet. Measured
# 2026-10-19 on In-Bangalore-1 and tracked as Omni #169.
#
# This client refuses the parameters rather than let a caller believe a sandbox
# is network-restricted when it is not. Failing open on an isolation control is
# worse than not offering one, because the caller cannot tell the difference.
# Remove this guard when enforcement ships, not before.
NETWORK_POLICY_ESCAPE_HATCH_ENV = "KRUTRIM_ALLOW_UNENFORCED_NETWORK_POLICY"

NETWORK_POLICY_UNENFORCED_MESSAGE = (
    "Sandbox network policy is accepted by the service but not enforced: outbound and "
    "inbound traffic remain unrestricted regardless of what you pass, and only the "
    "update response echoes the policy back (Omni #169, re-measured 2026-10-19). "
    "This client refuses these parameters rather than report a restriction that does "
    "not exist. Do not rely on them to isolate untrusted code. To send them anyway "
    "for service-side testing, set " + NETWORK_POLICY_ESCAPE_HATCH_ENV + "=1."
)


def validate_identifier(value: str) -> str:
    if not value:
        raise ValueError(f"Expected a non-empty sandbox identifier but received {value!r}")
    return value


def validate_required_path(path: str) -> str:
    if not path:
        raise ValueError(f"Expected a non-empty sandbox path but received {path!r}")
    return path


def validate_ttl(ttl_seconds: int) -> int:
    if not 60 <= ttl_seconds <= 604800:
        raise ValueError("Sandbox timeout must be between 60 and 604800 seconds")
    return ttl_seconds


def validate_sandbox_name(name: str) -> str:
    """Mirror the service's sandbox name rules so a bad name fails fast.

    The service caps the name at 28 characters and rejects a longer one with an
    HTTP 400. DNS-1035 itself permits 63, so the bound is ours to carry: without
    it a well-formed but long name costs a round trip to discover, and generated
    names (a prefix, a run id and a workload name) cross 28 easily.
    """
    if not DNS_1035_NAME.fullmatch(name):
        raise ValueError("sandbox_name must be a DNS-1035 lowercase name")
    if len(name) > MAX_SANDBOX_NAME_LEN:
        raise ValueError(
            f"sandbox_name must be at most {MAX_SANDBOX_NAME_LEN} characters, got {len(name)}"
        )
    return name


def validate_labels(labels: Mapping[str, str]) -> Mapping[str, str]:
    """Mirror the service's sandbox label rules so bad labels fail fast.

    Keys and values must stay free of the ``?labels=k=v,k2=v2`` selector
    delimiters so every label remains filterable.
    """
    if len(labels) > MAX_LABELS:
        raise ValueError(f"at most {MAX_LABELS} labels are allowed")
    for key, value in labels.items():
        if not key:
            raise ValueError("label keys cannot be empty")
        if len(key) > MAX_LABEL_KEY_LEN:
            raise ValueError(f"label key {key!r} exceeds {MAX_LABEL_KEY_LEN} characters")
        if len(value) > MAX_LABEL_VALUE_LEN:
            raise ValueError(f"label {key!r} value exceeds {MAX_LABEL_VALUE_LEN} characters")
        if "=" in key or "," in key:
            raise ValueError(f"label key {key!r} must not contain '=' or ','")
        if "," in value:
            raise ValueError(f"label {key!r} value must not contain ','")
    return labels


def serialize_label_selector(labels: Mapping[str, str]) -> str:
    """Serialize a labels filter into the service's ``k=v,k2=v2`` form."""
    validate_labels(labels)
    return ",".join(f"{key}={value}" for key, value in labels.items())


def validate_command(command: str, timeout_seconds: int) -> None:
    if not command or len(command) > 100000:
        raise ValueError("command must contain between 1 and 100000 characters")
    if not 1 <= timeout_seconds <= 270:
        raise ValueError("command timeout must be between 1 and 270 seconds")


def validate_port(port: int) -> int:
    if not 1024 <= port <= 65535:
        raise ValueError("port must be between 1024 and 65535")
    return port


def normalize_allowlist(value: str | Sequence[str], *, field: str) -> str:
    if isinstance(value, str):
        if not value.strip():
            raise ValueError(f"{field} must be a non-empty string")
        return value
    entries = [str(entry).strip() for entry in value]
    if not entries:
        raise ValueError(f"{field} must contain at least one entry")
    for entry in entries:
        if not entry:
            raise ValueError(f"{field} entries must be non-empty strings")
        if "," in entry:
            raise ValueError(f"{field} entries must not contain commas; pass separate entries instead")
    return ",".join(entries)


def validate_network_policy(
    *,
    allow_internet_access: bool | None,
    outbound_cidr_allowlist: str | Sequence[str] | None,
    outbound_domain_allowlist: str | Sequence[str] | None,
    inbound_cidr_allowlist: str | Sequence[str] | None,
) -> None:
    requested = (
        allow_internet_access,
        outbound_cidr_allowlist,
        outbound_domain_allowlist,
        inbound_cidr_allowlist,
    )
    if any(value is not None for value in requested) and not os.environ.get(
        NETWORK_POLICY_ESCAPE_HATCH_ENV
    ):
        raise NotImplementedError(NETWORK_POLICY_UNENFORCED_MESSAGE)
    if allow_internet_access is False and any(
        value is not None for value in (outbound_cidr_allowlist, outbound_domain_allowlist, inbound_cidr_allowlist)
    ):
        raise ValueError(
            "allow_internet_access=False blocks all sandbox traffic and cannot be combined with allowlists"
        )


def _validate_content_size(content: bytes) -> bytes:
    if len(content) > MAX_BODY_BYTES:
        raise ValueError("raw content exceeds the 100 MB service limit")
    return content


def normalize_file_content(content: SandboxFileContent) -> bytes:
    if isinstance(content, bytes):
        return _validate_content_size(content)
    if isinstance(content, os.PathLike):
        return _validate_content_size(Path(content).read_bytes())
    if isinstance(content, io.IOBase):
        data = content.read()
        if not isinstance(data, bytes):
            raise TypeError("binary file objects must return bytes")
        return _validate_content_size(data)
    raise TypeError("file content must be bytes, a binary file object, or a path-like object")


async def normalize_file_content_async(content: SandboxFileContent) -> bytes:
    if isinstance(content, bytes):
        return _validate_content_size(content)
    if isinstance(content, os.PathLike):
        return _validate_content_size(await anyio.Path(content).read_bytes())
    if isinstance(content, io.IOBase):
        file_object = content

        def read_file() -> bytes:
            data = file_object.read()
            if not isinstance(data, bytes):
                raise TypeError("binary file objects must return bytes")
            return data

        return _validate_content_size(await anyio.to_thread.run_sync(read_file))
    raise TypeError("file content must be bytes, a binary file object, or a path-like object")


def normalize_proxy_content(content: str | bytes | None) -> str | bytes | None:
    if content is None:
        return None
    encoded = content.encode("utf-8") if isinstance(content, str) else content
    _validate_content_size(encoded)
    return content
