# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from .volume_param import VolumeParam
from .policy_param import PolicyParam

__all__ = ["V1UpdateLaunchTemplateParams"]


class V1UpdateLaunchTemplateParams(TypedDict, total=False):
    template_id: Required[str]

    template_name: Required[str]

    boot_volume_size: Annotated[str, PropertyInfo(alias="bootVolumeSize")]

    policy: Iterable[PolicyParam]

    qos: Dict[str, object]

    vm_volume_disk_size: str

    volume_size: Annotated[Iterable[VolumeParam], PropertyInfo(alias="volumeSize")]

    x_region: str