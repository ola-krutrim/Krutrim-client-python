from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "CreateLoadBalancerParams",
    "LoadBalancerData",
    "Listener",
    "PoolData",
    "L7Policy",
    "L7Rule",
    "LoadBalancerType",
    "Protocol",
]

LoadBalancerType = Literal["ALB", "NLB"]
Protocol = Literal["HTTP", "HTTPS", "TCP", "UDP"]


class CreateLoadBalancerParams(TypedDict, total=False):
    loadbalancer_data: Required[LoadBalancerData]


class LoadBalancerData(TypedDict, total=False):
    name: Required[str]
    description: str
    floating_ip: Required[bool]
    vpc_id: Required[str]
    network_id: Required[str]
    vip_subnet_id: Required[str]
    type: Required[LoadBalancerType]
    flavor: Required[str]
    security_group_krns: Required[Iterable[str]]
    listeners: Required[Iterable[Listener]]


class Listener(TypedDict, total=False):
    name: Required[str]
    protocol: Required[Protocol]
    protocol_port: Required[int]
    default_pool: Required[bool]
    pool_data: Required[Iterable[PoolData]]
    l7_policies: Iterable[L7Policy]


class PoolData(TypedDict, total=False):
    name: Required[str]
    description: str
    algorithm: Required[str]
    protocol: Required[Protocol]
    target_group_name: Required[str]


class L7Policy(TypedDict, total=False):
    policy_name: Required[str]
    action: Required[str]
    position: Required[int]
    redirect_url: str
    rules: Required[Iterable[L7Rule]]


class L7Rule(TypedDict, total=False):
    type: Required[str]
    compare_type: Required[str]
    value: Required[str]
