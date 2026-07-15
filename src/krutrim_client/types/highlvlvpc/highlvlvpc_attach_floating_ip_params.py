
from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HighlvlvpcAttachFloatingIpParams"]


class HighlvlvpcAttachFloatingIpParams(TypedDict, total=False):
    """Body for POST /v1/highlvlvpc/attachFloatingIp."""

    attach_port: Required[str]
    """Port KRN to attach the floating IP to."""

    detach_port: Required[str]
    """Port KRN currently holding the floating IP (to detach from)."""
