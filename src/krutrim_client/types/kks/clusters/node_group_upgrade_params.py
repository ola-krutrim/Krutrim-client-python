# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["NodeGroupUpgradeParams", "ScalingConfig"]


class NodeGroupUpgradeParams(TypedDict, total=False):
    cluster_krn: Required[Annotated[str, PropertyInfo(alias="clusterKrn")]]

    scaling_config: Annotated[ScalingConfig, PropertyInfo(alias="scalingConfig")]


class ScalingConfig(TypedDict, total=False):
    desired_size: Annotated[int, PropertyInfo(alias="desiredSize")]

    max_size: Annotated[int, PropertyInfo(alias="maxSize")]

    min_size: Annotated[int, PropertyInfo(alias="minSize")]
