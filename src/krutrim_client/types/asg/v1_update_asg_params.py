# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo
from .policy_param import PolicyParam
from .volume_param import VolumeParam

__all__ = ["V1UpdateAsgParams"]


class V1UpdateAsgParams(TypedDict, total=False):
    asg_krn: str

    asg_name: str

    attach_floating_ip: bool

    boot_volume_size: Annotated[str, PropertyInfo(alias="bootVolumeSize")]

    image_krn: str

    instance_name: Annotated[str, PropertyInfo(alias="instanceName")]

    instance_type: Annotated[str, PropertyInfo(alias="instanceType")]

    instance_type_id: Annotated[str, PropertyInfo(alias="instanceTypeId")]

    max: int

    min: int

    network_krn: str

    policy: Iterable[PolicyParam]

    region: str

    save_as_template: bool

    security_groups: SequenceNotStr[str]

    sshkey_name: str

    subnet_id: str

    tags: Iterable[object]

    vm_volume_disk_size: str

    volume_name: Annotated[str, PropertyInfo(alias="volumeName")]

    volume_size: Annotated[Iterable[VolumeParam], PropertyInfo(alias="volumeSize")]

    vpc_krn: str