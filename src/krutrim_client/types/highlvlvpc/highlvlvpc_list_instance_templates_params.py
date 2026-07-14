
from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HighlvlvpcListInstanceTemplatesParams"]


class HighlvlvpcListInstanceTemplatesParams(TypedDict, total=False):
    """Query for GET /vm/v1/instance-templates/list."""

    page: int
    limit: int
