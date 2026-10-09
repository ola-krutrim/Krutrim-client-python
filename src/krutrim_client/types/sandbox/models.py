from typing import Any, Dict, List, Literal, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "NetworkStorageWorkflowInput",
    "PodTemplate",
    "TemplateListResponse",
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
    "SandboxNetworkPolicyData",
    "SandboxNetworkPolicyResponse",
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


class TemplateListResponse(List[PodTemplate]):
    """The result of ``list_templates``.

    Behaves exactly like a plain ``list`` of :class:`PodTemplate` objects
    (indexing, iteration, ``len()``, etc. all work as before), but also
    exposes ``model_dump()`` so it can be handled the same way as the other
    ``list_*`` response models on this resource (``list()`` ->
    ``SandboxListResponse``, ``list_flavors()`` -> ``FlavorListResponse``).
    """

    def model_dump(self, *args: Any, **kwargs: Any) -> List[Dict[str, Any]]:
        return [item.model_dump(*args, **kwargs) for item in self]

    def model_dump_json(self, *args: Any, **kwargs: Any) -> str:
        import json

        return json.dumps(self.model_dump(*args, **kwargs))


class FlavorGroupBy(BaseModel):
    flavorname: Optional[str] = None
    flavorid: Optional[str] = None
    flavorstatus: Optional[Literal["active", "inactive"]] = None
    availability: Optional[str] = None
    cost: Optional[float] = None
    currency: Optional[str] = None
    unit: Optional[str] = None
    type: Optional[str] = None
    vcpus: Optional[float] = None
    storage: Optional[float] = None
    local_disk: Optional[str] = None
    ram_size: Optional[float] = None
    vcpu_num: Optional[float] = None
    gpu_manufacturer_name: Optional[str] = None
    gpu_ram_size: Optional[float] = None
    gpu_resource_mapping: Optional[str] = None
    request_gpu_number: Optional[int] = None
    node_label: Optional[str] = None
    empheralcost: Optional[float] = None
    peristantcost: Optional[float] = None

    @property
    def flavor_status(self) -> Optional[Literal["active", "inactive"]]:
        """Backward-compatible alias for ``flavorstatus``."""
        return self.flavorstatus


class FlavorItem(BaseModel):
    subject: Optional[str] = None
    group_by: Optional[FlavorGroupBy] = FieldInfo(alias="groupBy", default=None)
    time: Optional[str] = None


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
    labels: Optional[Dict[str, str]] = None
    ttl_seconds: Optional[int] = FieldInfo(alias="ttlSeconds", default=None)
    expires_at: Optional[datetime] = FieldInfo(alias="expiresAt", default=None)
    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    updated_at: Optional[datetime] = FieldInfo(alias="updatedAt", default=None)

    @property
    def sandbox_id(self) -> Optional[str]:
        """Alias for ``id``.

        The high-level ``Sandbox`` wrapper returned by ``sandbox.create(...)``
        exposes the identifier as ``sandbox_id``. This model backs both
        ``list()`` rows and ``retrieve()``, which otherwise only expose ``id``,
        so the same attribute now works regardless of which call produced the
        object (see #143).
        """
        return self.id


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
    labels: Optional[Dict[str, str]] = None
    """Echo of the caller-supplied labels accepted at create."""

    @property
    def sandbox_id(self) -> Optional[str]:
        """Alias for ``id``, consistent with ``SandboxResponse.sandbox_id`` (see #143)."""
        return self.id


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

    @property
    def sandbox_id(self) -> Optional[str]:
        """Alias for ``id``, consistent with ``SandboxResponse.sandbox_id`` (see #143)."""
        return self.id


class SandboxDeleteResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SandboxDeleteData] = None


class SandboxTTLData(BaseModel):
    id: Optional[str] = None
    ttl_seconds: Optional[int] = FieldInfo(alias="ttlSeconds", default=None)
    expires_at: Optional[datetime] = FieldInfo(alias="expiresAt", default=None)

    @property
    def sandbox_id(self) -> Optional[str]:
        """Alias for ``id``, consistent with ``SandboxResponse.sandbox_id`` (see #143)."""
        return self.id


class SandboxTTLResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SandboxTTLData] = None


class SandboxNetworkPolicyData(BaseModel):
    id: Optional[str] = None
    allow_internet_access: Optional[bool] = FieldInfo(alias="allowInternetAccess", default=None)
    outbound_cidr_allowlist: Optional[str] = FieldInfo(alias="outboundCidrAllowlist", default=None)
    outbound_domain_allowlist: Optional[str] = FieldInfo(alias="outboundDomainAllowlist", default=None)
    inbound_cidr_allowlist: Optional[str] = FieldInfo(alias="inboundCidrAllowlist", default=None)

    @property
    def sandbox_id(self) -> Optional[str]:
        """Alias for ``id``, consistent with ``SandboxResponse.sandbox_id`` (see #143)."""
        return self.id


class SandboxNetworkPolicyResponse(BaseModel):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[SandboxNetworkPolicyData] = None


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
