from __future__ import annotations

from typing_extensions import Literal

import httpx

from ._common import PREFIX, prepare, _integer, identifier
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
    PortResponse,
    PortListResponse,
    PortCloseResponse,
)


class PortsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PortsResourceWithRawResponse:
        return PortsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PortsResourceWithStreamingResponse:
        return PortsResourceWithStreamingResponse(self)

    def expose(
        self,
        *,
        krn_id: str,
        x_region: str,
        port: int,
        access: Literal["token", "private"] | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PortResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/ports. Token URLs are credentials returned only by this call."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="ports.expose",
            x_region=x_region,
            body={"port": port, "access": access},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._post(f"{PREFIX}/sandboxes/{krn_id}/ports", cast_to=PortResponse, options=options, body=body)

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
    ) -> PortListResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/ports."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="ports.list",
            x_region=x_region,
            body={},
            query={"limit": limit, "offset": offset},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(f"{PREFIX}/sandboxes/{krn_id}/ports", cast_to=PortListResponse, options=options)

    def close(
        self,
        *,
        krn_id: str,
        port: int,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PortCloseResponse:
        """DELETE /sandbox/v1/sandboxes/{krn_id}/ports/{port}."""
        krn_id = identifier(krn_id, "krn_id")
        _integer(port, "port", 1, 65535)
        body, options = prepare(
            self._client,
            action="ports.close",
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
        return self._delete(
            f"{PREFIX}/sandboxes/{krn_id}/ports/{port}", cast_to=PortCloseResponse, options=options, body=body
        )


class AsyncPortsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPortsResourceWithRawResponse:
        return AsyncPortsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPortsResourceWithStreamingResponse:
        return AsyncPortsResourceWithStreamingResponse(self)

    async def expose(
        self,
        *,
        krn_id: str,
        x_region: str,
        port: int,
        access: Literal["token", "private"] | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PortResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/ports. Token URLs are credentials returned only by this call."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="ports.expose",
            x_region=x_region,
            body={"port": port, "access": access},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._post(f"{PREFIX}/sandboxes/{krn_id}/ports", cast_to=PortResponse, options=options, body=body)

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
    ) -> PortListResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/ports."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="ports.list",
            x_region=x_region,
            body={},
            query={"limit": limit, "offset": offset},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(f"{PREFIX}/sandboxes/{krn_id}/ports", cast_to=PortListResponse, options=options)

    async def close(
        self,
        *,
        krn_id: str,
        port: int,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PortCloseResponse:
        """DELETE /sandbox/v1/sandboxes/{krn_id}/ports/{port}."""
        krn_id = identifier(krn_id, "krn_id")
        _integer(port, "port", 1, 65535)
        body, options = prepare(
            self._client,
            action="ports.close",
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
        return await self._delete(
            f"{PREFIX}/sandboxes/{krn_id}/ports/{port}", cast_to=PortCloseResponse, options=options, body=body
        )


class PortsResourceWithRawResponse:
    def __init__(self, resource: PortsResource) -> None:
        self.expose = to_raw_response_wrapper(resource.expose)
        self.list = to_raw_response_wrapper(resource.list)
        self.close = to_raw_response_wrapper(resource.close)


class PortsResourceWithStreamingResponse:
    def __init__(self, resource: PortsResource) -> None:
        self.expose = to_streamed_response_wrapper(resource.expose)
        self.list = to_streamed_response_wrapper(resource.list)
        self.close = to_streamed_response_wrapper(resource.close)


class AsyncPortsResourceWithRawResponse:
    def __init__(self, resource: AsyncPortsResource) -> None:
        self.expose = async_to_raw_response_wrapper(resource.expose)
        self.list = async_to_raw_response_wrapper(resource.list)
        self.close = async_to_raw_response_wrapper(resource.close)


class AsyncPortsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncPortsResource) -> None:
        self.expose = async_to_streamed_response_wrapper(resource.expose)
        self.list = async_to_streamed_response_wrapper(resource.list)
        self.close = async_to_streamed_response_wrapper(resource.close)
