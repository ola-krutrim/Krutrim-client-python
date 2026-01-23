# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from .volume_param import VolumeParam

__all__ = ["V1UpdateLaunchTemplateParams", "Policy"]


class V1UpdateLaunchTemplateParams(TypedDict, total=False):
    template_id: Required[str]

    template_name: Required[str]

    boot_volume_size: Annotated[str, PropertyInfo(alias="bootVolumeSize")]

    policy: Iterable[Policy]

    qos: Dict[str, object]

    vm_volume_disk_size: str

    volume_size: Annotated[Iterable[VolumeParam], PropertyInfo(alias="volumeSize")]

    x_region: str


class Policy(TypedDict, total=False):
    predefined_metric_type: Annotated[str, PropertyInfo(alias="PredefinedMetricType")]

    scale_in_cooldown: Annotated[int, PropertyInfo(alias="ScaleInCooldown")]

    scale_in_threshold: Annotated[int, PropertyInfo(alias="ScaleInThreshold")]

    scale_out_cooldown: Annotated[int, PropertyInfo(alias="ScaleOutCooldown")]

    scale_out_threshold: Annotated[int, PropertyInfo(alias="ScaleOutThreshold")]