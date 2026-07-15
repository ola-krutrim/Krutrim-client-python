
from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["VolumeDetachParams", "VolumeDetachInput"]


class VolumeDetachInput(TypedDict, total=False):
    instanceId: Required[str]
    attachment_id: Required[str]


class VolumeDetachParams(TypedDict, total=False):
    """Body for POST /kbs/v1/volumes/{id}/action?op=detach."""

    input: Required[VolumeDetachInput]
