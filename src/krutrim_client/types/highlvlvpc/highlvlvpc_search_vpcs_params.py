#

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["HighlvlvpcSearchVpcsParams"]


class HighlvlvpcSearchVpcsParams(TypedDict, total=False):
    count: bool
    """Whether the API should include the total result count."""

    name: str
    """Filter VPCs by name."""

    order: str
    """Sort direction, such as ``asc`` or ``desc``."""

    page: int
    """Page number for pagination."""

    size: int
    """Number of items to return per page."""

    sort_by: str
    """Field used to sort the results."""

    status: str
    """Filter VPCs by status."""
