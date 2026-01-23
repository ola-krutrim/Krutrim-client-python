# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo
from .policy_param import PolicyParam
from .volume_param import VolumeParam

__all__ = ["V1CreateLaunchTemplateParams"]


class V1CreateLaunchTemplateParams(TypedDict, total=False):
    attach_floating_ip: bool

    boot_volume_size: Annotated[str, PropertyInfo(alias="bootVolumeSize")]

    image_krn: str

    instance_name: Annotated[str, PropertyInfo(alias="instanceName")]

    instance_type: Annotated[str, PropertyInfo(alias="instanceType")]

    max: int

    min: int

    network_krn: str

    policy: Iterable[PolicyParam]

    qos: Dict[str, object]

    region: str

    security_groups: SequenceNotStr[str]

    sshkey_name: str

    subnet_id: str

    template_name: str

    vm_volume_disk_size: str

    volume_name: Annotated[str, PropertyInfo(alias="volumeName")]

    volume_size: Annotated[Iterable[VolumeParam], PropertyInfo(alias="volumeSize")]

    volume_type: Annotated[str, PropertyInfo(alias="volumeType")]

    vpc_krn: str

    x_region: str