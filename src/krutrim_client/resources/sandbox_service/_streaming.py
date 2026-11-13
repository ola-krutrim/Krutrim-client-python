from __future__ import annotations

from typing import Dict, Iterator, AsyncIterator, cast
from typing_extensions import override

import anyio
import httpx
from pydantic import ValidationError

from ._exceptions import SandboxStreamError
from ..._streaming import Stream, AsyncStream, ServerSentEvent
from ...types.sandbox_service import ExecEvent, ExecExitEvent, ExecErrorEvent, ExecOutputEvent


def _event(sse: ServerSentEvent, response: httpx.Response) -> ExecEvent:
    try:
        data = sse.json()
        if not isinstance(data, dict):
            raise ValueError("Expected a JSON object")
        # The SSE event name is authoritative, not a JSON field supplied by the server.
        data = {**cast(Dict[str, object], data), "type": sse.event}
        if sse.event in ("stdout", "stderr"):
            return ExecOutputEvent.model_validate(data)
        if sse.event == "exit":
            return ExecExitEvent.model_validate(data)
        if sse.event == "error":
            error = ExecErrorEvent.model_validate(data)
            raise SandboxStreamError(error.error, event=error, response=response)
        raise ValueError(f"Unknown sandbox exec event: {sse.event!r}")
    except (ValueError, ValidationError) as exc:
        raise SandboxStreamError("Invalid sandbox exec event", event=sse, response=response) from exc


class SandboxExecStream(Stream[ExecEvent]):
    """Named exec events. Use as a context manager when stopping iteration early."""

    @override
    def __stream__(self) -> Iterator[ExecEvent]:
        try:
            for sse in self._iter_events():
                event = _event(sse, self.response)
                if isinstance(event, ExecExitEvent):
                    self.close()
                    yield event
                    return
                yield event
            raise SandboxStreamError("Sandbox exec stream ended before exit", response=self.response)
        except httpx.HTTPError as exc:
            raise SandboxStreamError("Sandbox exec stream disconnected before exit", response=self.response) from exc
        finally:
            self.close()


class AsyncSandboxExecStream(AsyncStream[ExecEvent]):
    """Async named exec events. Use as an async context manager for early exit."""

    @override
    async def __stream__(self) -> AsyncIterator[ExecEvent]:
        try:
            async for sse in self._iter_events():
                event = _event(sse, self.response)
                if isinstance(event, ExecExitEvent):
                    await self.close()
                    yield event
                    return
                yield event
            raise SandboxStreamError("Sandbox exec stream ended before exit", response=self.response)
        except httpx.HTTPError as exc:
            raise SandboxStreamError("Sandbox exec stream disconnected before exit", response=self.response) from exc
        finally:
            await self.close()

    @override
    async def close(self) -> None:
        # Keep response cleanup effective even when an enclosing task is cancelled.
        with anyio.CancelScope(shield=True):
            await super().close()
