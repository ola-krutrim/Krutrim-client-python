from __future__ import annotations

from ..._models import BaseModel

__all__ = ["DeleteTargetGroupResponse"]


class DeleteTargetGroupResponse(BaseModel):
    code: str
    message: str
