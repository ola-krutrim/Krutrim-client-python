# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from krutrim_client._utils import PropertyInfo

__all__ = ["HighlvlUpdateTargetGroupParams", "HealthMonitor", "Member"]


class HighlvlUpdateTargetGroupParams(TypedDict, total=False):
    x_region: Required[Annotated[str, PropertyInfo(alias="x-region")]]

    health_monitor: HealthMonitor

    members: Iterable[Member]

    target_group_name: str

    vpc_id: str


class HealthMonitor(TypedDict, total=False):
    delay: int

    h_type: str

    timeout: int

    url_path: str


class Member(TypedDict, total=False):
    address: str

    name: str

    protocol_port: int

    weight: int