from typing import Any, Dict, List, Literal, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "NetworkStorageWorkflowInput",
    "PodTemplate",
    "FlavorGroupBy",
    "FlavorItem",
    "FlavorListResponse",
    "SandboxResponse",
    "SandboxListData",
    "SandboxListResponse",
    "AsyncSandboxData",
    "AsyncSandboxResponse",
    "SandboxGetResponse",
    "SandboxDeleteData",
    "SandboxDeleteResponse",
    "SandboxTTLData",
    "SandboxTTLResponse",
    "SandboxFileData",
    "SandboxFileResponse",
    "SandboxEntryInfo",
    "SandboxEntryListResponse",
    "SandboxEntryResponse",
    "SandboxCommandResult",
    "SandboxCommandResponse",
    "SandboxPortInfo",
    "SandboxPortResponse",
    "SandboxPortListResponse",
]


class NetworkStorageWorkflowInput(BaseModel):
    network_storage_id: Optional[str] = FieldInfo(alias="networkStorageId", default=None)
    network_storage_mount_path: Optional[str] = FieldInfo(alias="networkStorageMountPath", default=None)
    network_storage_read_only: Optional[bool] = FieldInfo(alias="networkStorageReadOnly", default=None)


class PodTemplate(BaseModel):
    id: Optional[int] = FieldInfo(alias="ID", default=None)
    template_name: Optional[str] = None
    description: Optional[str] = None
    template_container_image_path: Optional[str] = None
    template_container_start_command: Optional[str] = None
    container_disk_size: Optional[str] = None
    volume_disk_size: Optional[str] = None
    volume_mount_path: Optional[str] = None
    expose_http_ports: Optional[str] = None
    expose_tcp_ports: Optional[str] = None
    environment_variables: Optional[str] = None
    enable_ssh: Optional[bool] = None
    enable_jupyter: Optional[bool] = None
    require_model_source: Optional[bool] = None
    health_check_path: Optional[str] = None
    supported_services: Optional[List[Literal["endpoint", "aipod", "sandbox"]]] = None
    template_type: Optional[Literal["official", "private"]] = None
    account_id: Optional[str] = None
    user_id: Optional[str] = None


class FlavorGroupBy(BaseModel):
    flavor_status: Optional[Literal["active", "inactive"]] = FieldInfo(alias="flavorStatus", default=None)


class FlavorItem(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    subject: Optional[str] = None
    group_by: Optional[FlavorGroupBy] = FieldInfo(alias="groupBy", default=None)
    resources: Optional[Dict[str, Any]] = None


class FlavorListResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[List[FlavorItem]] = None


class SandboxResponse(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    krn: Optional[str] = None
    status: Optional[Literal["deploying", "active", "deleting", "failed_deploy"]] = None
    error_message: Optional[str] = FieldInfo(alias="errorMessage", default=None)
    region: Optional[str] = None
    service_url: Optional[str] = FieldInfo(alias="serviceUrl", default=None)
    image_uri: Optional[str] = FieldInfo(alias="imageUri", default=None)
    flavor_name: Optional[str] = FieldInfo(alias="flavorName", default=None)
    memory: Optional[int] = None
    no_cpus: Optional[int] = FieldInfo(alias="noCpus", default=None)
    storage: Optional[int] = None
    no_gpus: Optional[int] = FieldInfo(alias="noGpus", default=None)
    gpu_type: Optional[str] = FieldInfo(alias="gpuType", default=None)
    network_storages: Optional[List[NetworkStorageWorkflowInput]] = FieldInfo(alias="networkStorages", default=None)
    environment_variables: Optional[Dict[str, str]] = FieldInfo(alias="environmentVariables", default=None)
    ttl_seconds: Optional[int] = FieldInfo(alias="ttlSeconds", default=None)
    expires_at: Optional[datetime] = FieldInfo(alias="expiresAt", default=None)
    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    updated_at: Optional[datetime] = FieldInfo(alias="updatedAt", default=None)


class SandboxListData(BaseModel):
    rows: Optional[List[SandboxResponse]] = None
    total: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    total_pages: Optional[int] = FieldInfo(alias="totalPages", default=None)


class SandboxListResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SandboxListData] = None


class AsyncSandboxData(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    krn: Optional[str] = None
    status: Optional[str] = None
    region: Optional[str] = None


class AsyncSandboxResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[AsyncSandboxData] = None


class SandboxGetResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SandboxResponse] = None


class SandboxDeleteData(BaseModel):
    id: Optional[str] = None


class SandboxDeleteResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SandboxDeleteData] = None


class SandboxTTLData(BaseModel):
    id: Optional[str] = None
    ttl_seconds: Optional[int] = FieldInfo(alias="ttlSeconds", default=None)
    expires_at: Optional[datetime] = FieldInfo(alias="expiresAt", default=None)


class SandboxTTLResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SandboxTTLData] = None


class SandboxFileData(BaseModel):
    path: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None


class SandboxFileResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SandboxFileData] = None


class SandboxEntryInfo(BaseModel):
    name: Optional[str] = None
    path: Optional[str] = None
    type: Optional[Literal["file", "dir"]] = None
    size: Optional[int] = None
    mode: Optional[str] = None
    modified_time: Optional[int] = FieldInfo(alias="modifiedTime", default=None)


class SandboxEntryListResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[List[SandboxEntryInfo]] = None


class SandboxEntryResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SandboxEntryInfo] = None


class SandboxCommandResult(BaseModel):
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = FieldInfo(alias="exitCode", default=None)
    stdout_truncated: Optional[bool] = FieldInfo(alias="stdoutTruncated", default=None)
    stderr_truncated: Optional[bool] = FieldInfo(alias="stderrTruncated", default=None)
    timed_out: Optional[bool] = FieldInfo(alias="timedOut", default=None)


class SandboxCommandResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SandboxCommandResult] = None


class SandboxPortInfo(BaseModel):
    port: Optional[int] = None
    status: Optional[Literal["provisioning", "active", "closing", "failed"]] = None
    error_message: Optional[str] = FieldInfo(alias="errorMessage", default=None)
    url: Optional[str] = None


class SandboxPortResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SandboxPortInfo] = None


class SandboxPortListResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[List[SandboxPortInfo]] = None
