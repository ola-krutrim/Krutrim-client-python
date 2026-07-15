
from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["HighlvlvpcUpdatePortSecurityGroupsParams"]


class HighlvlvpcUpdatePortSecurityGroupsParams(TypedDict, total=False):
    """Body for PUT /api/v1/ports/{port_krn}."""

    security_groups: Required[List[str]]
