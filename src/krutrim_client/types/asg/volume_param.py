# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict, Required

from ..._utils import PropertyInfo

__all__ = ["VolumeParam"]


class VolumeParam(TypedDict, total=False):
    count: Required[int]

    volume_name: Annotated[str, PropertyInfo(alias="volumeName")]

    volume_size: Required[Annotated[int, PropertyInfo(alias="volumeSize")]]

    volume_type: Annotated[str, PropertyInfo(alias="volumeType")]