# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import TypedDict

__all__ = ["RecordUpdateParams", "Record"]


class RecordUpdateParams(TypedDict, total=False):
    records: Iterable[Record]

    rname: str

    routing: str

    type: str


class Record(TypedDict, total=False):
    value: str
