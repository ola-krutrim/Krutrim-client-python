from __future__ import annotations

from typing import Optional

import httpx

from ..._exceptions import KrutrimClientError
from ...types.sandbox_service import OperationResponse


class SandboxOperationError(KrutrimClientError):
    """A queued operation failed. The complete last response is available as operation."""

    def __init__(self, operation: OperationResponse) -> None:
        self.operation = operation
        super().__init__(
            f"Sandbox operation {operation.details.id} failed: {operation.details.error or 'unknown error'}"
        )


class SandboxOperationTimeoutError(KrutrimClientError):
    """Polling expired; the server operation continues independently."""

    def __init__(self, operation_id: str, operation: Optional[OperationResponse]) -> None:
        self.operation_id = operation_id
        self.operation = operation
        super().__init__(f"Timed out waiting for sandbox operation {operation_id}")


class SandboxStreamError(KrutrimClientError):
    """Stream failure. A disconnected exec command may still be running."""

    def __init__(self, message: str, *, event: object = None, response: Optional[httpx.Response] = None) -> None:
        self.event = event
        self.response = response
        super().__init__(message)
