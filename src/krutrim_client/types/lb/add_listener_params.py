from __future__ import annotations

from typing_extensions import Required, TypedDict

from .create_load_balancer_params import Listener

__all__ = ["AddListenerParams", "Listener"]


class AddListenerParams(TypedDict, total=False):
    loadbalancer_krn: Required[str]
    listener: Required[Listener]
