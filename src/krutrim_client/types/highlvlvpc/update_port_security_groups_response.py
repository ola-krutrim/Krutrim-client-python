
from typing import Any, List, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["UpdatePortSecurityGroupsResponse", "UpdatedPort", "UpdatedPortFixedIp"]


class UpdatedPortFixedIp(BaseModel):
    subnet_id: Optional[str] = None
    ip_address: Optional[str] = None


class UpdatedPort(BaseModel):
    account_id: Optional[str] = None
    security_groups: Optional[List[str]] = None
    region: Optional[str] = None
    krn_id: Optional[str] = None
    k_customer_id: Optional[str] = None
    name: Optional[str] = None
    network_id: Optional[str] = None
    admin_state_up: Optional[bool] = None
    status: Optional[str] = None
    mac_address: Optional[str] = None
    fixed_ips: Optional[List[UpdatedPortFixedIp]] = None
    is_deleted: Optional[bool] = None
    allowed_address_pairs: Optional[List[Any]] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    device_id: Optional[str] = None
    device_owner: Optional[str] = None
    reqId: Optional[str] = None
    vpc_id: Optional[str] = None


class UpdatePortSecurityGroupsResponse(BaseModel):
    port: Optional[UpdatedPort] = None
