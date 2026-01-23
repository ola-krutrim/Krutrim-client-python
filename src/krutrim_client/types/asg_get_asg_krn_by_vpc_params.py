# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["AsgGetAsgKrnByVpcParams"]


class AsgGetAsgKrnByVpcParams(TypedDict, total=False):
    page: Required[int]

    size: Required[int]

    vpc_krn: Required[str]