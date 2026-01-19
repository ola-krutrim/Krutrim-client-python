from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._types import FileTypes
from ..._utils import PropertyInfo

__all__ = ["CertImportParams"]


class CertImportParams(TypedDict, total=False):
    cert_file: Annotated[FileTypes, PropertyInfo(alias="certFile")]

    flag: str

    name: str

    tags: str