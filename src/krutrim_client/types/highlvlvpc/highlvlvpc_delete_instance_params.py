
from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HighlvlvpcDeleteInstanceParams"]


class HighlvlvpcDeleteInstanceParams(TypedDict, total=False):
    """Query params for DELETE /vm/v1/delete_instance_async."""

    instanceKrn: Required[str]
    """The KRN of the instance to be deleted."""

    deleteVolume: Required[bool]
    """Whether to delete attached volumes with the instance."""
