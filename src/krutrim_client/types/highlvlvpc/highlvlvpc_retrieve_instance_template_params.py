
from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HighlvlvpcRetrieveInstanceTemplateParams"]


class HighlvlvpcRetrieveInstanceTemplateParams(TypedDict, total=False):
    """Query for GET /vm/v1/instance-templates/details."""

    template_krn: Required[str]
