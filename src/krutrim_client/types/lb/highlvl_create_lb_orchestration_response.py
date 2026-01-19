from __future__ import annotations
from typing import Optional, Any
from ..._models import BaseModel

class LBOrchestrationResp(BaseModel):
    lb_task_id: str
    message: str

