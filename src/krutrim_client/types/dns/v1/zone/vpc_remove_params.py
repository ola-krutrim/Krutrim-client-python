# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import TypedDict

__all__ = ["VpcRemoveParams", "Vpcinfo"]


class VpcRemoveParams(TypedDict, total=False):
    vpcinfo: Iterable[Vpcinfo]


class Vpcinfo(TypedDict, total=False):
    subnetid: str

    vpcid: str
