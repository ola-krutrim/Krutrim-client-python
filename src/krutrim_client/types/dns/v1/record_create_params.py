# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import TypedDict

__all__ = ["RecordCreateParams", "Record"]


class RecordCreateParams(TypedDict, total=False):
    krnid: str

    records: Iterable[Record]

    rname: str

    routing: str

    ttl: int

    type: str


class Record(TypedDict, total=False):
    value: str

    weight: int
