
from __future__ import annotations

from typing import List, Union, Optional, Any
from typing_extensions import Required, TypedDict

from ..._types import Base64FileInput


__all__ = ["HighlvlvpcCreateInstanceParams"]


class HighlvlvpcCreateInstanceParams(TypedDict, total=False):
    """Body for POST /vm/v1/create_instance_async."""

    instanceName: Required[str]
    instanceType: Required[str]
    region: Required[str]
    security_groups: Required[List[str]]
    sshkey_name: Required[str]
    subnet_id: Required[str]
    vpc_id: Required[str]

    image_krn: Optional[str]
    floating_ip: bool
    user_data: Union[str, Base64FileInput]
    volume_name: Optional[str]
    volume_size: Optional[int]
    volumetype: Optional[str]
    delete_on_termination: bool
    port_krn: str
    isGpu: bool
    volumes: List[Any]
    tags: List[Any]
    count: int
    easydeploy_type: str
    gateway_password: str
    model_name: str
    model_api_key: str
