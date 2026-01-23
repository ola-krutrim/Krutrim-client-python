# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ClusterCreateParams", "KubernetesNetworkConfig", "ResourcesVpcConfig"]


class ClusterCreateParams(TypedDict, total=False):
    kubernetes_network_config: Annotated[KubernetesNetworkConfig, PropertyInfo(alias="kubernetesNetworkConfig")]

    name: str

    resources_vpc_config: Annotated[ResourcesVpcConfig, PropertyInfo(alias="resourcesVpcConfig")]

    version: str


class KubernetesNetworkConfig(TypedDict, total=False):
    pod_ipv4_cidr: Annotated[str, PropertyInfo(alias="podIpv4Cidr")]

    service_ipv4_cidr: Annotated[str, PropertyInfo(alias="serviceIpv4Cidr")]


class ResourcesVpcConfig(TypedDict, total=False):
    subnet_krns: Annotated[str, PropertyInfo(alias="subnetKrns")]

    vpc_krn: Annotated[str, PropertyInfo(alias="vpcKrn")]
