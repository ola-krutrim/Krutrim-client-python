# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ...._types import SequenceNotStr
from ...._utils import PropertyInfo

__all__ = ["NodeGroupCreateParams", "NodeRepairConfig", "RemoteAccess", "ScalingConfig"]


class NodeGroupCreateParams(TypedDict, total=False):
    disk_size: Annotated[int, PropertyInfo(alias="diskSize")]

    instance_types: Annotated[str, PropertyInfo(alias="instanceTypes")]

    name: str

    node_repair_config: Annotated[NodeRepairConfig, PropertyInfo(alias="nodeRepairConfig")]

    remote_access: Annotated[RemoteAccess, PropertyInfo(alias="remoteAccess")]

    scaling_config: Annotated[ScalingConfig, PropertyInfo(alias="scalingConfig")]

    subnets_krn: Annotated[str, PropertyInfo(alias="subnetsKrn")]


class NodeRepairConfig(TypedDict, total=False):
    enabled: bool


class RemoteAccess(TypedDict, total=False):
    source_security_groups_krns: Annotated[SequenceNotStr[str], PropertyInfo(alias="sourceSecurityGroupsKrns")]

    ssh_key_krn: Annotated[str, PropertyInfo(alias="sshKeyKrn")]


class ScalingConfig(TypedDict, total=False):
    desired_size: Annotated[int, PropertyInfo(alias="desiredSize")]

    max_size: Annotated[int, PropertyInfo(alias="maxSize")]

    min_size: Annotated[int, PropertyInfo(alias="minSize")]
