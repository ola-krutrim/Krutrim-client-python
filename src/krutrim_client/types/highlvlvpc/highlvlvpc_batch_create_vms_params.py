
from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HighlvlvpcBatchCreateVmsParams"]


class HighlvlvpcBatchCreateVmsParams(TypedDict, total=False):
    """Body for POST /vm/v1/batch-vm-create."""

    template_krn: Required[str]
    count: Required[int]
    instanceName: Required[str]
