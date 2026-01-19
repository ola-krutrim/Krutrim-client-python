# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .v1 import (
    V1Resource,
    AsyncV1Resource,
    V1ResourceWithRawResponse,
    AsyncV1ResourceWithRawResponse,
    V1ResourceWithStreamingResponse,
    AsyncV1ResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["InternalResource", "AsyncInternalResource"]


class InternalResource(SyncAPIResource):
    @cached_property
    def v1(self) -> V1Resource:
        return V1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> InternalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#accessing-raw-response-data-eg-headers
        """
        return InternalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InternalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#with_streaming_response
        """
        return InternalResourceWithStreamingResponse(self)


class AsyncInternalResource(AsyncAPIResource):
    @cached_property
    def v1(self) -> AsyncV1Resource:
        return AsyncV1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncInternalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#accessing-raw-response-data-eg-headers
        """
        return AsyncInternalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInternalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#with_streaming_response
        """
        return AsyncInternalResourceWithStreamingResponse(self)


class InternalResourceWithRawResponse:
    def __init__(self, internal: InternalResource) -> None:
        self._internal = internal

    @cached_property
    def v1(self) -> V1ResourceWithRawResponse:
        return V1ResourceWithRawResponse(self._internal.v1)


class AsyncInternalResourceWithRawResponse:
    def __init__(self, internal: AsyncInternalResource) -> None:
        self._internal = internal

    @cached_property
    def v1(self) -> AsyncV1ResourceWithRawResponse:
        return AsyncV1ResourceWithRawResponse(self._internal.v1)


class InternalResourceWithStreamingResponse:
    def __init__(self, internal: InternalResource) -> None:
        self._internal = internal

    @cached_property
    def v1(self) -> V1ResourceWithStreamingResponse:
        return V1ResourceWithStreamingResponse(self._internal.v1)


class AsyncInternalResourceWithStreamingResponse:
    def __init__(self, internal: AsyncInternalResource) -> None:
        self._internal = internal

    @cached_property
    def v1(self) -> AsyncV1ResourceWithStreamingResponse:
        return AsyncV1ResourceWithStreamingResponse(self._internal.v1)
