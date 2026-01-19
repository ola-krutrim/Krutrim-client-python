# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HighlvlDeleteTargetGroupParams"]


class HighlvlDeleteTargetGroupParams(TypedDict, total=False):
    target_group_name: Required[str]

    vpc_id: Required[str]