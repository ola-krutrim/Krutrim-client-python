# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["AddonInstallParams"]


class AddonInstallParams(TypedDict, total=False):
    addon_name: Annotated[str, PropertyInfo(alias="addonName")]