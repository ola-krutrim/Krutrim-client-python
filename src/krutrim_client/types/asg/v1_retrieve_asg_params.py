# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["V1RetrieveAsgParams"]


class V1RetrieveAsgParams(TypedDict, total=False):
    page: Required[int]

    size: Required[int]

    asg_krn: str

    asg_name: str

    x_region: Annotated[str, PropertyInfo(alias="x-region")]