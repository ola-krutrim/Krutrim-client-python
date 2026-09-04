from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ._helpers import validate_port, validate_identifier
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.sandbox import SandboxPortResponse, SandboxPortListResponse

__all__ = ["PortsResource", "AsyncPortsResource"]


class PortsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PortsResourceWithRawResponse:
        return PortsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PortsResourceWithStreamingResponse:
        return PortsResourceWithStreamingResponse(self)

    def open(
        self,
        sandbox_id: str,
        port: int,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxPortResponse:
        validate_identifier(sandbox_id)
        validate_port(port)
        return self._post(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/ports",
            cast_to=SandboxPortResponse,
            body={"port": port},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    def list(
        self,
        sandbox_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxPortListResponse:
        validate_identifier(sandbox_id)
        return self._get(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/ports",
            cast_to=SandboxPortListResponse,
            options=make_request_options(extra_headers=extra_headers, extra_query=extra_query, timeout=timeout),
        )

    def close(
        self,
        sandbox_id: str,
        port: int,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        validate_identifier(sandbox_id)
        validate_port(port)
        return self._delete(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/ports/{port}",
            cast_to=NoneType,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )


class AsyncPortsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPortsResourceWithRawResponse:
        return AsyncPortsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPortsResourceWithStreamingResponse:
        return AsyncPortsResourceWithStreamingResponse(self)

    async def open(
        self,
        sandbox_id: str,
        port: int,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxPortResponse:
        validate_identifier(sandbox_id)
        validate_port(port)
        return await self._post(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/ports",
            cast_to=SandboxPortResponse,
            body={"port": port},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    async def list(
        self,
        sandbox_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxPortListResponse:
        validate_identifier(sandbox_id)
        return await self._get(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/ports",
            cast_to=SandboxPortListResponse,
            options=make_request_options(extra_headers=extra_headers, extra_query=extra_query, timeout=timeout),
        )

    async def close(
        self,
        sandbox_id: str,
        port: int,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        validate_identifier(sandbox_id)
        validate_port(port)
        return await self._delete(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/ports/{port}",
            cast_to=NoneType,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )


class PortsResourceWithRawResponse:
    def __init__(self, ports: PortsResource) -> None:
        self.open = to_raw_response_wrapper(ports.open)
        self.list = to_raw_response_wrapper(ports.list)
        self.close = to_raw_response_wrapper(ports.close)


class AsyncPortsResourceWithRawResponse:
    def __init__(self, ports: AsyncPortsResource) -> None:
        self.open = async_to_raw_response_wrapper(ports.open)
        self.list = async_to_raw_response_wrapper(ports.list)
        self.close = async_to_raw_response_wrapper(ports.close)


class PortsResourceWithStreamingResponse:
    def __init__(self, ports: PortsResource) -> None:
        self.open = to_streamed_response_wrapper(ports.open)
        self.list = to_streamed_response_wrapper(ports.list)
        self.close = to_streamed_response_wrapper(ports.close)


class AsyncPortsResourceWithStreamingResponse:
    def __init__(self, ports: AsyncPortsResource) -> None:
        self.open = async_to_streamed_response_wrapper(ports.open)
        self.list = async_to_streamed_response_wrapper(ports.list)
        self.close = async_to_streamed_response_wrapper(ports.close)
