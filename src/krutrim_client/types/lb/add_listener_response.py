from __future__ import annotations

from typing import Optional

from ..._models import BaseModel

__all__ = ["AddListenerResponse"]


class AddListenerResponse(BaseModel):
    code: str
    message: str
    details: Optional[object] = None
