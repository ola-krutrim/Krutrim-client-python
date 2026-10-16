from __future__ import annotations

from typing import List

from ..._models import BaseModel

__all__ = ["UpdateTargetGroupResponse", "UpdateTargetGroupDetails"]


class UpdateTargetGroupDetails(BaseModel):
    loadbalancer_krn: List[str]
    members: List[str]
    req_id: str
    target_group_krn: str
    target_group_name: str
    vpc_krn: str


class UpdateTargetGroupResponse(BaseModel):
    code: str
    message: str
    details: UpdateTargetGroupDetails
