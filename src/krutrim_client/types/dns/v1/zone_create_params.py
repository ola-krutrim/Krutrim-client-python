# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["ZoneCreateParams"]


class ZoneCreateParams(TypedDict, total=False):
    subnetid: str

    type: Literal["public", "private"]

    vpcid: str

    zonename: str
