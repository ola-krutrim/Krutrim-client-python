from __future__ import annotations

import io
import os
import re
from typing import Mapping
from pathlib import Path

import anyio

from ...types.sandbox import SandboxFileContent

MAX_BODY_BYTES = 100 * 1024 * 1024
DNS_1035_NAME = re.compile(r"^[a-z]([-a-z0-9]*[a-z0-9])?$")
MAX_LABELS = 16
MAX_LABEL_KEY_LEN = 63
MAX_LABEL_VALUE_LEN = 255


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
    if not DNS_1035_NAME.fullmatch(name):
        raise ValueError("sandbox_name must be a DNS-1035 lowercase name")
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
