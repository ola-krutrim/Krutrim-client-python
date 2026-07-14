
from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["HighlvlvpcCreateInstanceTemplateParams"]


class HighlvlvpcCreateInstanceTemplateParams(TypedDict, total=False):
    """Body for POST /vm/v1/instance-templates/create."""

    name: Required[str]
    vpc_id: Required[str]
    subnet_id: Required[str]
    instanceType: Required[str]
    sshkey_name: Required[str]
    region: Required[str]
    image_krn: Required[str]
    volumetype: Required[str]
    volume_size: Required[int]
    volume_name: Required[str]
    security_groups: Required[List[str]]
    isGpu: bool
    user_data: str
