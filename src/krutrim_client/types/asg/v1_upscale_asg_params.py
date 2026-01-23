# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["V1UpscaleAsgParams"]


class V1UpscaleAsgParams(TypedDict, total=False):
    asg_krn: str

    attach_floating_ip: bool

    desired_vm_count: int

    vpc_krn: str