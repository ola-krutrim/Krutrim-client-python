from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "UpdateLoadBalancerParams",
    "ListenerUpdate",
    "LoadBalancerUpdate",
    "PolicyOperation",
    "RuleOperation",
    "PoolUpdate",
    "Operation",
]

Operation = Literal["create", "update", "delete"]


class UpdateLoadBalancerParams(TypedDict, total=False):
    loadbalancer_krn: Required[str]
    listener_krn: str
    listener: ListenerUpdate
    loadbalancer: LoadBalancerUpdate
    policy: Iterable[PolicyOperation]
    rules: Iterable[RuleOperation]
    pool: Iterable[PoolUpdate]


class ListenerUpdate(TypedDict, total=False):
    operation: Required[Operation]
    name: str
    sni_container_refs: Iterable[str]


class LoadBalancerUpdate(TypedDict, total=False):
    description: str
    security_group_krn: Iterable[str]


class PolicyOperation(TypedDict, total=False):
    operation: Required[Operation]
    krn: str
    name: str
    action: str
    description: str
    redirect_pool_name: str
    redirect_url: str
    redirect_http_code: int
    position: int
    admin_state_up: bool
    tags: Iterable[str]


class RuleOperation(TypedDict, total=False):
    operation: Required[Operation]
    krn: str
    policy_krn: str
    rule_type: str
    compare_type: str
    key: str
    value: str


class PoolUpdate(TypedDict, total=False):
    krn: str
    name: str
    algorithm: str
    target_group_krn: str
