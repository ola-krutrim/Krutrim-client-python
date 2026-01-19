# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["TagListParams"]


class TagListParams(TypedDict, total=False):
    cert_id: Required[Annotated[str, PropertyInfo(alias="certId")]]

    tag_name: Required[Annotated[str, PropertyInfo(alias="tagName")]]