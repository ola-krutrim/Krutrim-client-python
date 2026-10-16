from __future__ import annotations

from typing import List

from ..._models import BaseModel

__all__ = ["CreateTargetGroupResponse", "CreateTargetGroupDetails"]


class CreateTargetGroupDetails(BaseModel):
    target_group_krn: str
    req_id: str
    name: str
    k_customer_id: str
    x_account_id: str
    region: str
    loadbalancer_krn: List[str]
    vpc_krn: str
    health_monitor: str
    members: List[str]


class CreateTargetGroupResponse(BaseModel):
    code: str
    message: str
    details: CreateTargetGroupDetails
