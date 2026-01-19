from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["CertListParams"]


class CertListParams(TypedDict, total=False):
    vpc_id: Required[Annotated[str, PropertyInfo(alias="vpcId")]]

    lbtype: str