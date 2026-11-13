"""Typed request bodies. Omitted fields use service defaults."""

from __future__ import annotations

from typing import Dict, List
from typing_extensions import Literal, Required, TypedDict


class EgressParams(TypedDict, total=False):
    default_action: Required[Literal["allow", "deny"]]
    allow: List[str]
    deny: List[str]


class NetworkPolicyParams(TypedDict, total=False):
    egress: EgressParams


class SandboxCreateParams(TypedDict, total=False):
    name: Required[str]
    flavor: Required[str]
    template: str
    image: str
    ttl_seconds: int
    env: Dict[str, str]
    network: NetworkPolicyParams


class TemplateCreateParams(TypedDict, total=False):
    name: Required[str]
    image: Required[str]
    description: str


class ExecParams(TypedDict, total=False):
    cmd: Required[str]
    cwd: str
    env: Dict[str, str]
    stdin: str
    user: str
    timeout_seconds: int
    stream: bool


class CommandCreateParams(TypedDict, total=False):
    cmd: Required[str]
    cwd: str
    env: Dict[str, str]
    user: str
    timeout_seconds: int


class SandboxExtendParams(TypedDict):
    ttl_seconds: int


class SandboxResizeParams(TypedDict):
    flavor: str


class PortExposeParams(TypedDict, total=False):
    port: Required[int]
    access: Literal["token", "private"]
