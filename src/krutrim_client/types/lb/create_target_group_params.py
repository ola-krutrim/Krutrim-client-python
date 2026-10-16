from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["CreateTargetGroupParams", "HealthMonitor", "Member"]


class CreateTargetGroupParams(TypedDict, total=False):
    target_group_name: Required[str]
    vpc_krn: Required[str]
    lb_krn: Required[Iterable[str]]
    members: Required[Iterable[Member]]
    health_monitor: Required[HealthMonitor]


class Member(TypedDict, total=False):
    name: Required[str]
    address: Required[str]
    protocol_port: Required[int]
    weight: Required[int]


class HealthMonitor(TypedDict, total=False):
    delay: Required[int]
    timeout: Required[int]
    max_retries: Required[int]
    health_check_path: Required[str]
    type: Required[str]
    name: Required[str]
