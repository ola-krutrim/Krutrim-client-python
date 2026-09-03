from __future__ import annotations

from os import PathLike
from typing import IO, Any, List, Union, Mapping
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = [
    "NetworkStorageAttachmentInput",
    "SandboxCreateParams",
    "SandboxListParams",
    "SandboxSetTTLParams",
    "SandboxFileListParams",
    "SandboxFileMoveParams",
    "SandboxCommandRunParams",
    "SandboxPortOpenParams",
    "SandboxProxyRequestParams",
    "SandboxFileContent",
]


SandboxFileContent = Union[bytes, IO[bytes], PathLike[str]]


class NetworkStorageAttachmentInput(TypedDict, total=False):
    network_storage_id: Required[Annotated[str, PropertyInfo(alias="networkStorageId")]]
    network_storage_mount_path: Annotated[str, PropertyInfo(alias="networkStorageMountPath")]


class SandboxCreateParams(TypedDict, total=False):
    sandbox_name: Required[Annotated[str, PropertyInfo(alias="sandboxName")]]
    region: Required[str]
    flavor_name: Required[Annotated[str, PropertyInfo(alias="flavorName")]]
    template_id: Annotated[int, PropertyInfo(alias="templateId")]
    template_name: Annotated[str, PropertyInfo(alias="templateName")]
    network_storages: Annotated[List[NetworkStorageAttachmentInput], PropertyInfo(alias="networkStorages")]
    environment_variables: Annotated[Mapping[str, str], PropertyInfo(alias="environmentVariables")]
    ttl_seconds: Annotated[int, PropertyInfo(alias="ttlSeconds")]


class SandboxListParams(TypedDict, total=False):
    region: str
    status: str
    name: str
    page: int
    limit: int


class SandboxSetTTLParams(TypedDict, total=False):
    ttl_seconds: Required[Annotated[int, PropertyInfo(alias="ttlSeconds")]]


class SandboxFileListParams(TypedDict, total=False):
    path: str
    depth: int


class SandboxFileMoveParams(TypedDict, total=False):
    path: Required[str]
    new_path: Required[Annotated[str, PropertyInfo(alias="newPath")]]


class SandboxCommandRunParams(TypedDict, total=False):
    cmd: Required[str]
    cwd: str
    envs: Mapping[str, str]
    timeout_seconds: Annotated[int, PropertyInfo(alias="timeoutSeconds")]


class SandboxPortOpenParams(TypedDict, total=False):
    port: Required[int]


class SandboxProxyRequestParams(TypedDict, total=False):
    method: Required[str]
    path: Required[str]
    query: Mapping[str, object]
    headers: Mapping[str, str]
    json: Any
    content: str | bytes
    max_retries: int
