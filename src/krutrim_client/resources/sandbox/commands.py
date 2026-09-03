from __future__ import annotations

from typing import Mapping

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ._helpers import validate_command, validate_identifier
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.sandbox import SandboxCommandResponse, SandboxCommandRunParams

__all__ = ["CommandsResource", "AsyncCommandsResource"]


class CommandsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CommandsResourceWithRawResponse:
        return CommandsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CommandsResourceWithStreamingResponse:
        return CommandsResourceWithStreamingResponse(self)

    def run(
        self,
        sandbox_id: str,
        command: str,
        *,
        cwd: str | None = None,
        envs: Mapping[str, str] | None = None,
        timeout_seconds: int = 60,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxCommandResponse:
        validate_identifier(sandbox_id)
        validate_command(command, timeout_seconds)
        body: dict[str, object] = {"cmd": command, "timeout_seconds": timeout_seconds}
        if cwd is not None:
            body["cwd"] = cwd
        if envs is not None:
            body["envs"] = envs
        return self._post(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/commands",
            cast_to=SandboxCommandResponse,
            body=maybe_transform(body, SandboxCommandRunParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )


class AsyncCommandsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCommandsResourceWithRawResponse:
        return AsyncCommandsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCommandsResourceWithStreamingResponse:
        return AsyncCommandsResourceWithStreamingResponse(self)

    async def run(
        self,
        sandbox_id: str,
        command: str,
        *,
        cwd: str | None = None,
        envs: Mapping[str, str] | None = None,
        timeout_seconds: int = 60,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxCommandResponse:
        validate_identifier(sandbox_id)
        validate_command(command, timeout_seconds)
        body: dict[str, object] = {"cmd": command, "timeout_seconds": timeout_seconds}
        if cwd is not None:
            body["cwd"] = cwd
        if envs is not None:
            body["envs"] = envs
        return await self._post(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/commands",
            cast_to=SandboxCommandResponse,
            body=await async_maybe_transform(body, SandboxCommandRunParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )


class CommandsResourceWithRawResponse:
    def __init__(self, commands: CommandsResource) -> None:
        self.run = to_raw_response_wrapper(commands.run)


class AsyncCommandsResourceWithRawResponse:
    def __init__(self, commands: AsyncCommandsResource) -> None:
        self.run = async_to_raw_response_wrapper(commands.run)


class CommandsResourceWithStreamingResponse:
    def __init__(self, commands: CommandsResource) -> None:
        self.run = to_streamed_response_wrapper(commands.run)


class AsyncCommandsResourceWithStreamingResponse:
    def __init__(self, commands: AsyncCommandsResource) -> None:
        self.run = async_to_streamed_response_wrapper(commands.run)
