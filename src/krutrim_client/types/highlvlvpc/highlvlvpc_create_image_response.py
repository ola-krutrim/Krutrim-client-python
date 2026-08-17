from __future__ import annotations

from ..._models import BaseModel

__all__ = ["HighlvlvpcCreateImageResponse"]


class HighlvlvpcCreateImageResponse(BaseModel):
    image: str
    """The image ID or URL returned by the API"""
