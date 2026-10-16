from __future__ import annotations

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["ListLoadBalancersResponse", "LoadBalancerListDetails", "LoadBalancerSummary", "Pagination"]


class LoadBalancerSummary(BaseModel):
    lb_krn: str
    lb_name: str
    lb_type: str
    flavor: str
    provisioning_status: str
    operating_status: str
    status: str
    vip_address: str
    floating_ip: Optional[str] = None
    created_on: int


class Pagination(BaseModel):
    current_page: int
    total_pages: int
    total_count: int
    page: int
    limit: int
    offset: int


class LoadBalancerListDetails(BaseModel):
    loadbalancers: List[LoadBalancerSummary]
    pagination: Pagination


class ListLoadBalancersResponse(BaseModel):
    code: str
    message: str
    details: LoadBalancerListDetails
