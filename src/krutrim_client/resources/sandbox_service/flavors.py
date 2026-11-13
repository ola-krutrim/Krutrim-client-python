from __future__ import annotations

import httpx

from ._common import PREFIX, prepare
from ..._types import NOT_GIVEN, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.sandbox_service import (
    FlavorListResponse,
)


class FlavorsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FlavorsResourceWithRawResponse:
        return FlavorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FlavorsResourceWithStreamingResponse:
        return FlavorsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        x_region: str,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FlavorListResponse:
        """GET /sandbox/v1/flavors."""
        _body, options = prepare(
            self._client,
            action="flavors.list",
            x_region=x_region,
            body={},
            query={"limit": limit, "offset": offset},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(f"{PREFIX}/flavors", cast_to=FlavorListResponse, options=options)


class AsyncFlavorsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFlavorsResourceWithRawResponse:
        return AsyncFlavorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFlavorsResourceWithStreamingResponse:
        return AsyncFlavorsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        x_region: str,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FlavorListResponse:
        """GET /sandbox/v1/flavors."""
        _body, options = prepare(
            self._client,
            action="flavors.list",
            x_region=x_region,
            body={},
            query={"limit": limit, "offset": offset},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(f"{PREFIX}/flavors", cast_to=FlavorListResponse, options=options)


class FlavorsResourceWithRawResponse:
    def __init__(self, resource: FlavorsResource) -> None:
        self.list = to_raw_response_wrapper(resource.list)


class FlavorsResourceWithStreamingResponse:
    def __init__(self, resource: FlavorsResource) -> None:
        self.list = to_streamed_response_wrapper(resource.list)


class AsyncFlavorsResourceWithRawResponse:
    def __init__(self, resource: AsyncFlavorsResource) -> None:
        self.list = async_to_raw_response_wrapper(resource.list)


class AsyncFlavorsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncFlavorsResource) -> None:
        self.list = async_to_streamed_response_wrapper(resource.list)
