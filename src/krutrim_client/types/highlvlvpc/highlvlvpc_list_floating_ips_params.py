
from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HighlvlvpcListFloatingIpsParams"]


class HighlvlvpcListFloatingIpsParams(TypedDict, total=False):
    """Query for GET /v1/highlvlvpc/floating_ip_list."""

    vpc_id: Required[str]
