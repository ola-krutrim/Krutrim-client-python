from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["CertRetrieveParams"]


class CertRetrieveParams(TypedDict, total=False):
    cert_id: Required[Annotated[str, PropertyInfo(alias="certId")]]