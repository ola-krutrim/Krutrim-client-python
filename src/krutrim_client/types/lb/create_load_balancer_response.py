from __future__ import annotations

from ..._models import BaseModel

__all__ = ["CreateLoadBalancerResponse"]


class CreateLoadBalancerResponse(BaseModel):
    code: str
    message: str
    details: str
