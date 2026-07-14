
from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HighlvlvpcDeleteInstanceTemplateParams"]


class HighlvlvpcDeleteInstanceTemplateParams(TypedDict, total=False):
    """Query for DELETE /vm/v1/instance-templates/delete."""

    template_krn: Required[str]
