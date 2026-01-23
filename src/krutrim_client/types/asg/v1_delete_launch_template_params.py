# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["V1DeleteLaunchTemplateParams"]


class V1DeleteLaunchTemplateParams(TypedDict, total=False):
    template_id: Required[str]

    template_name: Required[str]

    version: Required[int]

    x_region: Required[Annotated[str, PropertyInfo(alias="x-region")]]