from __future__ import annotations

from typing import List
from datetime import datetime

from ..._models import BaseModel

__all__ = [
    "ListTargetGroupsResponse",
    "TargetGroup",
    "TargetGroupMember",
    "TargetGroupHealthCheck",
]


class TargetGroupMember(BaseModel):
    name: str
    address: str
    port: int
    weight: int
    operating_status: str
    type: str


class TargetGroupHealthCheck(BaseModel):
    name: str
    protocol: str
    path: str
    delay: int
    timeout: int
    max_retries: int


class TargetGroup(BaseModel):
    name: str
    target_group_krn: str
    target_type: str
    load_balancers: List[str]
    members: List[TargetGroupMember]
    health_check: TargetGroupHealthCheck
    vpc_krn: str
    created_at: datetime


class ListTargetGroupsResponse(BaseModel):
    code: str
    message: str
    details: List[TargetGroup]
