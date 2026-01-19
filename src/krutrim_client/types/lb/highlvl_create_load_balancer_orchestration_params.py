# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from krutrim_client._utils import PropertyInfo

__all__ = ["HighlvlCreateLoadBalancerOrchestrationParams"]


class HighlvlCreateLoadBalancerOrchestrationParams(TypedDict, total=False):
    k_customer_id: Required[Annotated[str, PropertyInfo(alias="k-customer-id")]]

    x_account_id: Required[Annotated[str, PropertyInfo(alias="x-account-id")]]

    x_region: Required[Annotated[str, PropertyInfo(alias="x-region")]]

    listeners: Iterable[object]

    loadbalancer_data: object