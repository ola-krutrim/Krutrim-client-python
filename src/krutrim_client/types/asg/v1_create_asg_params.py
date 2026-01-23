# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Annotated, TypedDict, Required

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo
from .policy_param import PolicyParam
from .volume_param import VolumeParam

__all__ = ["V1CreateAsgParams"]


class V1CreateAsgParams(TypedDict, total=False):
    asg_name: Required[str]

    image_krn: Required[str]

    instance_name: Required[Annotated[str, PropertyInfo(alias="instanceName")]]

    body_instance_type_1: Required[Annotated[str, PropertyInfo(alias="instanceType")]]

    instance_type_id: Required[Annotated[str, PropertyInfo(alias="instanceTypeId")]]

    max: Required[int]

    min: Required[int]

    network_krn: Required[str]

    region: Required[str]

    sshkey_name: Required[str]

    subnet_id: Required[str]

    volume_type: Required[Annotated[str, PropertyInfo(alias="volumeType")]]
    """Root / default volume type"""

    vpc_krn: Required[str]

    x_region: Required[Annotated[str, PropertyInfo(alias="x-region")]]

    attach_floating_ip: bool

    boot_volume_size: Annotated[str, PropertyInfo(alias="bootVolumeSize")]

    body_instance_type_2: Annotated[str, PropertyInfo(alias="instance_type")]

    launch_from_template: bool

    policy: Iterable[PolicyParam]

    body_save_as_template_1: Annotated[bool, PropertyInfo(alias="save_as_template")]

    body_save_as_template_2: Annotated[bool, PropertyInfo(alias="saveAsTemplate")]

    security_group_rules_name: str

    security_group_rules_port: str

    security_group_rules_protocol: str

    security_groups: SequenceNotStr[str]

    tags: Iterable[object]

    template_name: str

    vm_volume_disk_size: str

    volume_name: Annotated[str, PropertyInfo(alias="volumeName")]

    volume_size: Annotated[Iterable[VolumeParam], PropertyInfo(alias="volumeSize")]

    vpc_name: str
