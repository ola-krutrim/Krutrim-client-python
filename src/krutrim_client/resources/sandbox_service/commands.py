from __future__ import annotations

from typing import Dict

import httpx

from ._common import PREFIX, prepare, identifier
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.sandbox_service import (
    CommandResponse,
    CommandListResponse,
    CommandOutputResponse,
)


class CommandsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CommandsResourceWithRawResponse:
        return CommandsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CommandsResourceWithStreamingResponse:
        return CommandsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        krn_id: str,
        x_region: str,
        cmd: str,
        cwd: str | NotGiven = NOT_GIVEN,
        env: Dict[str, str] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        timeout_seconds: int | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommandResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/commands."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="commands.create",
            x_region=x_region,
            body={"cmd": cmd, "cwd": cwd, "env": env, "user": user, "timeout_seconds": timeout_seconds},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._post(f"{PREFIX}/sandboxes/{krn_id}/commands", cast_to=CommandResponse, options=options, body=body)

    def list(
        self,
        *,
        krn_id: str,
        x_region: str,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommandListResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/commands."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="commands.list",
            x_region=x_region,
            body={},
            query={"limit": limit, "offset": offset},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(f"{PREFIX}/sandboxes/{krn_id}/commands", cast_to=CommandListResponse, options=options)

    def retrieve(
        self,
        *,
        krn_id: str,
        command_id: str,
        x_region: str,
        stdout_offset: int | NotGiven = NOT_GIVEN,
        stderr_offset: int | NotGiven = NOT_GIVEN,
        max_bytes: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommandOutputResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/commands/{command_id}."""
        krn_id = identifier(krn_id, "krn_id")
        command_id = identifier(command_id, "command_id")
        _body, options = prepare(
            self._client,
            action="commands.retrieve",
            x_region=x_region,
            body={},
            query={"stdout_offset": stdout_offset, "stderr_offset": stderr_offset, "max_bytes": max_bytes},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(
            f"{PREFIX}/sandboxes/{krn_id}/commands/{command_id}", cast_to=CommandOutputResponse, options=options
        )

    def kill(
        self,
        *,
        krn_id: str,
        command_id: str,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommandResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/commands/{command_id}/kill."""
        krn_id = identifier(krn_id, "krn_id")
        command_id = identifier(command_id, "command_id")
        body, options = prepare(
            self._client,
            action="commands.kill",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._post(
            f"{PREFIX}/sandboxes/{krn_id}/commands/{command_id}/kill",
            cast_to=CommandResponse,
            options=options,
            body=body,
        )


class AsyncCommandsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCommandsResourceWithRawResponse:
        return AsyncCommandsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCommandsResourceWithStreamingResponse:
        return AsyncCommandsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        krn_id: str,
        x_region: str,
        cmd: str,
        cwd: str | NotGiven = NOT_GIVEN,
        env: Dict[str, str] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        timeout_seconds: int | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommandResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/commands."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="commands.create",
            x_region=x_region,
            body={"cmd": cmd, "cwd": cwd, "env": env, "user": user, "timeout_seconds": timeout_seconds},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._post(
            f"{PREFIX}/sandboxes/{krn_id}/commands", cast_to=CommandResponse, options=options, body=body
        )

    async def list(
        self,
        *,
        krn_id: str,
        x_region: str,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommandListResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/commands."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="commands.list",
            x_region=x_region,
            body={},
            query={"limit": limit, "offset": offset},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(f"{PREFIX}/sandboxes/{krn_id}/commands", cast_to=CommandListResponse, options=options)

    async def retrieve(
        self,
        *,
        krn_id: str,
        command_id: str,
        x_region: str,
        stdout_offset: int | NotGiven = NOT_GIVEN,
        stderr_offset: int | NotGiven = NOT_GIVEN,
        max_bytes: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommandOutputResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/commands/{command_id}."""
        krn_id = identifier(krn_id, "krn_id")
        command_id = identifier(command_id, "command_id")
        _body, options = prepare(
            self._client,
            action="commands.retrieve",
            x_region=x_region,
            body={},
            query={"stdout_offset": stdout_offset, "stderr_offset": stderr_offset, "max_bytes": max_bytes},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(
            f"{PREFIX}/sandboxes/{krn_id}/commands/{command_id}", cast_to=CommandOutputResponse, options=options
        )

    async def kill(
        self,
        *,
        krn_id: str,
        command_id: str,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommandResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/commands/{command_id}/kill."""
        krn_id = identifier(krn_id, "krn_id")
        command_id = identifier(command_id, "command_id")
        body, options = prepare(
            self._client,
            action="commands.kill",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._post(
            f"{PREFIX}/sandboxes/{krn_id}/commands/{command_id}/kill",
            cast_to=CommandResponse,
            options=options,
            body=body,
        )


class CommandsResourceWithRawResponse:
    def __init__(self, resource: CommandsResource) -> None:
        self.create = to_raw_response_wrapper(resource.create)
        self.list = to_raw_response_wrapper(resource.list)
        self.retrieve = to_raw_response_wrapper(resource.retrieve)
        self.kill = to_raw_response_wrapper(resource.kill)


class CommandsResourceWithStreamingResponse:
    def __init__(self, resource: CommandsResource) -> None:
        self.create = to_streamed_response_wrapper(resource.create)
        self.list = to_streamed_response_wrapper(resource.list)
        self.retrieve = to_streamed_response_wrapper(resource.retrieve)
        self.kill = to_streamed_response_wrapper(resource.kill)


class AsyncCommandsResourceWithRawResponse:
    def __init__(self, resource: AsyncCommandsResource) -> None:
        self.create = async_to_raw_response_wrapper(resource.create)
        self.list = async_to_raw_response_wrapper(resource.list)
        self.retrieve = async_to_raw_response_wrapper(resource.retrieve)
        self.kill = async_to_raw_response_wrapper(resource.kill)


class AsyncCommandsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncCommandsResource) -> None:
        self.create = async_to_streamed_response_wrapper(resource.create)
        self.list = async_to_streamed_response_wrapper(resource.list)
        self.retrieve = async_to_streamed_response_wrapper(resource.retrieve)
        self.kill = async_to_streamed_response_wrapper(resource.kill)
