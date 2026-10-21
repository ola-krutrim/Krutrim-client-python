from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["NodeGroupUpdateConfigParams", "ScalingConfig"]


class NodeGroupUpdateConfigParams(TypedDict, total=False):
    scaling_config: Required[Annotated[ScalingConfig, PropertyInfo(alias="scalingConfig")]]


class ScalingConfig(TypedDict, total=False):
    desired_size: Annotated[int, PropertyInfo(alias="desiredSize")]

    max_size: Annotated[int, PropertyInfo(alias="maxSize")]

    min_size: Annotated[int, PropertyInfo(alias="minSize")]
