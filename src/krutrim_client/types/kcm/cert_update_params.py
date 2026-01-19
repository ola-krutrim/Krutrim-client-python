from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._types import FileTypes
from ..._utils import PropertyInfo

__all__ = ["CertUpdateParams"]


class CertUpdateParams(TypedDict, total=False):
    x_vpc_id: Required[Annotated[str, PropertyInfo(alias="X-Vpc-Id")]]

    cert_file: Annotated[FileTypes, PropertyInfo(alias="certFile")]

    flag: str