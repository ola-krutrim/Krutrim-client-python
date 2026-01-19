# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from krutrim_client._utils import PropertyInfo

__all__ = ["HighlvlUpdateLoadBalancerParams"]


class HighlvlUpdateLoadBalancerParams(TypedDict, total=False):
    x_region: Required[Annotated[str, PropertyInfo(alias="x-region")]]


    listeners: Iterable[object]

    loadbalancer_data: object