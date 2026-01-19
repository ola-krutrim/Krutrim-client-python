from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["CertGetExpiringParams"]


class CertGetExpiringParams(TypedDict, total=False):
    date: Required[str]

    vpc_id: Required[Annotated[str, PropertyInfo(alias="vpcId")]]