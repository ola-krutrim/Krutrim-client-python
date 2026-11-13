"""Customer-facing sandbox response models. Times are Unix seconds unless documented otherwise."""

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field

from ..._models import BaseModel

SandboxStatus: TypeAlias = Literal[
    "PROVISIONING", "ACTIVE", "STOPPING", "DOWN", "STARTING", "RESIZING", "DELETING", "FAILED", "LOST"
]


class Egress(BaseModel):
    default_action: Literal["allow", "deny"]
    allow: Optional[List[str]] = None
    deny: Optional[List[str]] = None


class NetworkPolicy(BaseModel):
    egress: Optional[Egress] = None


class Port(BaseModel):
    port: int
    access: Literal["token", "private"]
    created_at: float
    proxy_url: Optional[str] = None
    url: Optional[str] = None
    """Credential URL returned only when a token port is exposed. Store it securely."""


class Sandbox(BaseModel):
    krn_id: str
    name: str
    status: SandboxStatus
    is_deleted: bool
    flavor: str
    vcpus: int
    mem_mib: int
    cpu_millis: Optional[int] = None
    disk_mib: Optional[int] = None
    template: str
    image: Optional[str] = None
    workdir: Optional[str] = None
    user: Optional[str] = None
    ttl_seconds: int
    created_at: float
    expires_at: float
    updated_at: float
    env: List[str]
    """Environment variable names only; values are never returned."""
    account_id: str
    customer_id: str
    region: str
    tenant: Optional[str] = None
    billing_id: Optional[str] = None
    last_operation: Optional[str] = None
    operation_id: Optional[str] = None
    last_error: Optional[str] = None
    network: Optional[NetworkPolicy] = None
    ports: Optional[List[Port]] = None
    timing_ms: Optional[Dict[str, float]] = None


class FlavorSize(BaseModel):
    flavor: str
    vcpus: int
    mem_mib: int
    cpu_millis: Optional[int] = None
    disk_mib: Optional[int] = None


class ResizeSpec(BaseModel):
    from_: FlavorSize = Field(alias="from")
    to: FlavorSize
    running: bool


class Operation(BaseModel):
    id: str
    state: Literal["pending", "running", "succeeded", "failed"]
    type: str
    attempts: int
    resize: Optional[ResizeSpec] = None
    krn_id: Optional[str] = None
    template: Optional[str] = None
    error: Optional[str] = None
    account_id: str
    customer_id: str
    region: str
    created_at: float
    updated_at: float
    finished_at: Optional[float] = None


class Template(BaseModel):
    krn_id: str
    id: str
    default_template: bool
    custom: bool
    status: str
    description: Optional[str] = None
    version: Optional[str] = None
    min_vcpus: Optional[float] = None
    min_mem_mib: Optional[int] = None
    image: Optional[str] = None
    build_error: Optional[str] = None
    created_at: Optional[float] = None
    operation_id: Optional[str] = None


class Flavor(BaseModel):
    id: str
    name: str
    vcpus: float
    ram_gib: float
    local_disk_gib: float
    cost: float
    currency: str
    unit: str
    region: str


class ExecResult(BaseModel):
    krn_id: Optional[str] = None
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float
    timed_out: bool = False
    truncated: bool = False


class Command(BaseModel):
    command_id: str
    krn_id: str
    cmd: str
    user: str
    pid: int
    status: Literal["running", "exited", "killed", "timed_out", "lost"]
    started_at: float
    cwd: Optional[str] = None
    timeout_seconds: Optional[int] = None
    exit_code: Optional[int] = None
    finished_at: Optional[float] = None
    error: Optional[str] = None
    account_id: Optional[str] = None
    customer_id: Optional[str] = None
    region: Optional[str] = None


class CommandOutput(BaseModel):
    command: Command
    stdout: str
    stderr: str
    stdout_offset: int
    stderr_offset: int
    stdout_size: int
    stderr_size: int


class FileUpload(BaseModel):
    name: str
    path: str
    size_bytes: int
    sha256: str
    type: Optional[str] = None


class TerminalTicket(BaseModel):
    krn_id: str
    ticket: str
    url: str
    expires_at: str
    """RFC 3339 timestamp; unlike other service timestamps, this is a string."""


class UsageInterval(BaseModel):
    flavor: str
    started_at: float
    seconds: int
    vcpus: Optional[int] = None
    mem_mib: Optional[int] = None
    stopped_at: Optional[float] = None


class UsageEvent(BaseModel):
    id: str
    operation: str
    at: float
    source: str
    billed: bool
    flavor: Optional[str] = None


class FlavorUsage(BaseModel):
    flavor: str
    seconds: int
    vcpu_seconds: int
    mem_mib_seconds: int
    vcpus: Optional[int] = None
    mem_mib: Optional[int] = None


class Usage(BaseModel):
    krn_id: str
    name: str
    account_id: str
    customer_id: str
    region: str
    metering_status: str
    running_seconds: int
    vcpu_seconds: int
    mem_mib_seconds: int
    by_flavor: List[FlavorUsage]
    intervals: List[UsageInterval]
    events: List[UsageEvent]
    closed: bool
    closed_at: Optional[float] = None
    updated_at: float
    flavor: Optional[str] = None
    running_since: Optional[float] = None


class Page(BaseModel):
    total: int
    limit: int
    offset: int


class SandboxPage(Page):
    sandboxes: List[Sandbox]


class TemplatePage(Page):
    default: str
    templates: List[Template]


class FlavorPage(Page):
    flavors: List[Flavor]


class CommandPage(Page):
    krn_id: str
    commands: List[Command]


class PortPage(Page):
    ports: List[Port]


class TemplateDeleted(BaseModel):
    id: str
    krn_id: str
    status: Literal["deleted"]


class PortClosed(BaseModel):
    krn_id: str
    port: int
    status: Literal["closed"]


class Envelope(BaseModel):
    code: str
    message: Optional[str] = None


class SandboxResponse(Envelope):
    details: Sandbox


class SandboxListResponse(Envelope):
    details: SandboxPage


class TemplateResponse(Envelope):
    details: Template


class TemplateListResponse(Envelope):
    details: TemplatePage


class TemplateDeleteResponse(Envelope):
    details: TemplateDeleted


class FlavorListResponse(Envelope):
    details: FlavorPage


class OperationResponse(Envelope):
    details: Operation


class ExecResponse(Envelope):
    details: ExecResult


class CommandResponse(Envelope):
    details: Command


class CommandListResponse(Envelope):
    details: CommandPage


class CommandOutputResponse(Envelope):
    details: CommandOutput


class FileUploadResponse(Envelope):
    details: FileUpload


class NetworkEnforcement(BaseModel):
    status: Literal["pending", "applied", "failed"]
    applied_at: Optional[float] = None


class NetworkDetails(NetworkPolicy):
    enforcement: Optional[NetworkEnforcement] = None
    operation_id: Optional[str] = None


class NetworkResponse(Envelope):
    details: NetworkDetails


class PortResponse(Envelope):
    details: Port


class PortListResponse(Envelope):
    details: PortPage


class PortCloseResponse(Envelope):
    details: PortClosed


class TerminalTicketResponse(Envelope):
    details: TerminalTicket


class UsageResponse(Envelope):
    details: Usage


class ExecOutputEvent(BaseModel):
    type: Literal["stdout", "stderr"]
    data: str


class ExecExitEvent(BaseModel):
    type: Literal["exit"]
    exit_code: int
    timed_out: bool = False
    duration_ms: float


class ExecErrorEvent(BaseModel):
    type: Literal["error"]
    error: str
