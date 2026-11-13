from __future__ import annotations

import re
import math
import ipaddress
import unicodedata
from uuid import uuid4
from typing import TYPE_CHECKING, Dict, Mapping, cast
from urllib.parse import quote

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, RequestOptions
from ..._utils import is_list
from ..._base_client import make_request_options

if TYPE_CHECKING:
    from ..._client import KrutrimClient, AsyncKrutrimClient

PREFIX = "/sandbox/v1"
STATUSES = {"PROVISIONING", "ACTIVE", "STOPPING", "DOWN", "STARTING", "RESIZING", "DELETING", "FAILED", "LOST"}


def identifier(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or any(unicodedata.category(c) == "Cc" for c in value):
        raise ValueError(f"{name} must be a non-empty string without control characters")
    if value in (".", ".."):
        raise ValueError(f"{name} must not be a dot path segment")
    return quote(value, safe=":")


def _integer(value: object, name: str, minimum: int, maximum: int) -> None:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{name} must be an integer {minimum}..{maximum}")


def positive_seconds(value: object, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a positive finite number")


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")


def _path(value: object, name: str, *, components: bool = False) -> None:
    if not isinstance(value, str) or not value.startswith("/") or len(value.encode()) > 4096:
        raise ValueError(f"{name} must be an absolute guest path of at most 4096 bytes")
    if any(unicodedata.category(c) == "Cc" for c in value):
        raise ValueError(f"{name} must not contain control characters")
    if components and any(len(c.encode()) > 255 for c in value.split("/")):
        raise ValueError("path components must not exceed 255 bytes")


def _network(value: object) -> None:
    if not isinstance(value, Mapping):
        raise ValueError("network must be an object")
    if not value:
        return
    policy = cast(Mapping[str, object], value)
    egress = policy.get("egress")
    if not isinstance(egress, Mapping):
        raise ValueError("network.egress must be an object")
    egress = cast(Mapping[str, object], egress)
    if egress.get("default_action") not in ("allow", "deny"):
        raise ValueError("network.egress.default_action must be allow or deny")
    for field in ("allow", "deny"):
        rules = egress.get(field, [])
        if not is_list(rules) or len(rules) > 64:
            raise ValueError(f"network.egress.{field} must contain at most 64 destinations")
        for rule in rules:
            if not isinstance(rule, str) or not rule:
                raise ValueError("network destinations must be non-empty strings")
            try:
                address = ipaddress.ip_network(rule, strict=False)
            except ValueError:
                domain = rule[2:] if rule.startswith("*.") else rule
                domain = domain[:-1] if domain.endswith(".") else domain
                if len(domain) > 253 or not all(
                    re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label) for label in domain.split(".")
                ):
                    raise ValueError(
                        "network destinations must be IPv4 addresses, CIDRs, domains, or *.domains"
                    ) from None
            else:
                if address.version != 4:
                    raise ValueError("IPv6 network rules are not supported")
    # Platform-specific blocked ranges remain the server's responsibility.


def _validate(action: str, body: Dict[str, object], query: Dict[str, object]) -> None:
    for key, maximum in (
        ("limit", 200),
        ("offset", 2**63 - 1),
        ("stdout_offset", 1 << 62),
        ("stderr_offset", 1 << 62),
    ):
        if key in query:
            _integer(query[key], key, 0, maximum)
    if "max_bytes" in query:
        _integer(query["max_bytes"], "max_bytes", 1, 1048576)
    if "status" in query and query["status"] not in STATUSES and query["status"] != "":
        raise ValueError("status must be a sandbox lifecycle status")
    if "path" in query:
        _path(query["path"], "path", components=True)
    for key in ("flavor", "image", "cmd"):
        if key in body:
            _text(body[key], key)
    if action == "sandboxes.create":
        if not isinstance(body.get("name"), str) or not re.fullmatch(
            r"[A-Za-z0-9](?:[A-Za-z0-9._-]{0,62}[A-Za-z0-9])?", str(body["name"])
        ):
            raise ValueError(
                "name must be 1..64 letters, digits, '.', '_' or '-', starting and ending with a letter or digit"
            )
        if body.get("template") and body.get("image"):
            raise ValueError("Pass template or image, not both")
        if "template" in body:
            _text(body["template"], "template")
    if action == "templates.create":
        name = body.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]{1,39}", name) or name.startswith("img-"):
            raise ValueError(
                "template name must be 2..40 lowercase letters, digits or '-', start with a letter, and not start with img-"
            )
    if "ttl_seconds" in body:
        _integer(body["ttl_seconds"], "ttl_seconds", 60, 604800)
    if "timeout_seconds" in body:
        maximum = 604800 if action == "commands.create" else 3600 if action == "sandboxes.exec_stream" else 120
        _integer(body["timeout_seconds"], "timeout_seconds", 1, maximum)
    if "cwd" in body and body["cwd"] != "":
        _path(body["cwd"], "cwd")
    if "user" in body and (
        not isinstance(body["user"], str)
        or not re.fullmatch(r"(?:[a-z_][a-z0-9_-]{0,31}|[0-9]{1,10})?", str(body["user"]))
    ):
        raise ValueError("user must be a Linux user name or numeric uid")
    if "stdin" in body and (not isinstance(body["stdin"], str) or len(str(body["stdin"]).encode()) > 1048576):
        raise ValueError("stdin must be a string of at most 1 MiB")
    if "env" in body:
        env = body["env"]
        if not isinstance(env, Mapping):
            raise ValueError("env must be a mapping")
        env = cast(Mapping[object, object], env)
        if len(env) > 64:
            raise ValueError("env must be a mapping of at most 64 variables")
        total_bytes = 0
        for env_name, env_value in env.items():
            if (
                not isinstance(env_name, str)
                or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,127}", env_name)
                or not isinstance(env_value, str)
            ):
                raise ValueError("env must map valid variable names to string values")
            reserved = (
                ("KRUTRIM_", "SPACE_")
                if action == "sandboxes.create"
                else ("KRUTRIM_",)
                if action == "commands.create"
                else ()
            )
            if env_name.startswith(reserved):
                raise ValueError("env variable name uses a reserved prefix")
            total_bytes += len(env_name.encode()) + len(env_value.encode())
        if total_bytes > 32768:
            raise ValueError("env must contain at most 32 KiB")
    if "network" in body:
        _network(body["network"])
    if action == "network.update":
        _network(body)
    if "port" in body:
        _integer(body["port"], "port", 1, 65535)
    if "access" in body and body["access"] not in ("token", "private"):
        raise ValueError("access must be token or private")
    if action in ("sandboxes.exec", "sandboxes.exec_stream") and body.get("stream", False) != (
        action == "sandboxes.exec_stream"
    ):
        raise ValueError("Use exec_stream for streaming and exec for buffered execution")


def prepare(
    client: KrutrimClient | AsyncKrutrimClient,
    *,
    action: str,
    x_region: str,
    body: Dict[str, object],
    query: Dict[str, object],
    extra_headers: Headers | None,
    extra_query: Query | None,
    extra_body: Body | None,
    timeout: float | httpx.Timeout | None | NotGiven,
    mutation: bool = False,
    unsafe: bool = False,
    idempotency_key: str | None = None,
) -> tuple[Dict[str, object], RequestOptions]:
    _text(x_region, "x_region")
    if not re.fullmatch(r"[A-Za-z](?:[A-Za-z0-9-]{0,62}[A-Za-z0-9])?", x_region):
        raise ValueError("x_region must be a region name of at most 64 characters")
    body = {k: v for k, v in body.items() if not isinstance(v, NotGiven)}
    query = {k: v for k, v in query.items() if not isinstance(v, NotGiven)}
    if extra_body is not None:
        if not isinstance(extra_body, Mapping):
            raise ValueError("extra_body must be a JSON object")
        body.update(cast(Mapping[str, object], extra_body))
    query.update(extra_query or {})
    _validate(action, body, query)
    headers: Headers = {"x-region": x_region, **(extra_headers or {})}
    # Resolve case-insensitively, including defaults, without disturbing SDK wrapper headers.
    effective = {k.lower(): v for k, v in client.default_headers.items()}
    effective.update({k.lower(): v for k, v in headers.items()})
    header_key = effective.get("idempotency-key")
    if unsafe and (isinstance(header_key, str) or idempotency_key is not None):
        raise ValueError("Idempotency-Key is not supported for this sandbox operation")
    if mutation:
        if idempotency_key is not None and isinstance(header_key, str) and header_key != idempotency_key:
            raise ValueError("Conflicting idempotency keys")
        key = (
            idempotency_key
            if idempotency_key is not None
            else header_key
            if isinstance(header_key, str)
            else str(uuid4())
        )
        _text(key, "idempotency_key")
        if not 1 <= len(key) <= 255 or any(not 33 <= ord(c) <= 126 for c in key):
            raise ValueError("idempotency_key must contain 1..255 printable ASCII characters without spaces")
        headers = {k: v for k, v in headers.items() if k.lower() != "idempotency-key"}
        headers["Idempotency-Key"] = key
    # Remove differently-cased defaults before adding overrides; HTTP header names are case-insensitive.
    unique = {name.lower(): (name, value) for name, value in headers.items()}
    resolved: Dict[str, str | Omit] = {name: Omit() for name in client.default_headers if name.lower() in unique}
    resolved.update({name: value for name, value in unique.values()})
    options = make_request_options(extra_headers=resolved, query=query, timeout=timeout)
    if unsafe:
        options["max_retries"] = 0
    return body, options
