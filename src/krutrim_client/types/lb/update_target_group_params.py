from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["UpdateTargetGroupParams", "HealthMonitor", "Member"]


class UpdateTargetGroupParams(TypedDict, total=False):
    krn: Required[str]
    members: Iterable[Member]
    health_monitor: HealthMonitor


class Member(TypedDict, total=False):
    name: Required[str]
    weight: Required[int]
    address: Required[str]
    protocol_port: Required[int]


class HealthMonitor(TypedDict, total=False):
    delay: Required[int]
    timeout: Required[int]
    max_retries: Required[int]
    health_check_path: Required[str]
    name: Required[str]
    type: str
