
from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HighlvlvpcGetInstanceTaskStatusParams"]


class HighlvlvpcGetInstanceTaskStatusParams(TypedDict, total=False):
    task_id: Required[str]
    """The task ID of the instance operation (create/delete)."""
