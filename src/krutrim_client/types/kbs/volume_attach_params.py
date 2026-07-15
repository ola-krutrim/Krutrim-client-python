
from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["VolumeAttachParams", "VolumeAttachInput"]


class VolumeAttachInput(TypedDict, total=False):
    instanceId: Required[str]
    mountPartition: str


class VolumeAttachParams(TypedDict, total=False):
    """Body for POST /kbs/v1/volumes/{id}/action?op=attach."""

    input: Required[VolumeAttachInput]
