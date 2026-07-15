
from typing import List, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = [
    "FloatingIpInfo",
    "FloatingIpList",
    "CreatePortResponse",
    "AttachFloatingIpResponse",
]


class FloatingIpInfo(BaseModel):
    floating_ip_address: Optional[str] = None
    floating_ip_krn: Optional[str] = None
    ip_version: Optional[int] = None
    port_krn: Optional[str] = None
    subnet_name: Optional[str] = None
    visibility: Optional[str] = None
    vm_name: Optional[str] = None


FloatingIpList: TypeAlias = List[FloatingIpInfo]


class CreatePortResponse(BaseModel):
    """Response from POST /v1/highlvlvpc/create_port (reserve floating IP)."""

    floating_ip_address: Optional[str] = None
    floating_ip_krn: Optional[str] = None
    message: Optional[str] = None
    port_krn: Optional[str] = None


class AttachFloatingIpResponse(BaseModel):
    message: Optional[str] = None
