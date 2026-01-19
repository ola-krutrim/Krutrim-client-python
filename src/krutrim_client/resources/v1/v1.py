# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .record import (
    RecordResource,
    AsyncRecordResource,
    RecordResourceWithRawResponse,
    AsyncRecordResourceWithRawResponse,
    RecordResourceWithStreamingResponse,
    AsyncRecordResourceWithStreamingResponse,
)
from ..._types import Body, Query, Headers, NoneType, NotGiven, NOT_GIVEN
from .zone.zone import (
    ZoneResource,
    AsyncZoneResource,
    ZoneResourceWithRawResponse,
    AsyncZoneResourceWithRawResponse,
    ZoneResourceWithStreamingResponse,
    AsyncZoneResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def zone(self) -> ZoneResource:
        return ZoneResource(self._client)

    @cached_property
    def record(self) -> RecordResource:
        return RecordResource(self._client)

    @cached_property
    def with_raw_response(self) -> V1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#accessing-raw-response-data-eg-headers
        """
        return V1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> V1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#with_streaming_response
        """
        return V1ResourceWithStreamingResponse(self)

    def get_nameserver_ip(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Get Name Server IP"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/dns/v1/nameserverip",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get_records(
        self,
        zoneid: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get Records for a Zone

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zoneid:
            raise ValueError(f"Expected a non-empty value for `zoneid` but received {zoneid!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/dns/v1/records/{zoneid}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get_service_health(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Get Service Health"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/dns/v1/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get_service_metrics(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Get Service Metrics"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/dns/v1/metrics",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list_zones(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Get All Zones"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/dns/v1/zones",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def zone(self) -> AsyncZoneResource:
        return AsyncZoneResource(self._client)

    @cached_property
    def record(self) -> AsyncRecordResource:
        return AsyncRecordResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncV1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#accessing-raw-response-data-eg-headers
        """
        return AsyncV1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncV1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#with_streaming_response
        """
        return AsyncV1ResourceWithStreamingResponse(self)

    async def get_nameserver_ip(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Get Name Server IP"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/dns/v1/nameserverip",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_records(
        self,
        zoneid: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get Records for a Zone

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zoneid:
            raise ValueError(f"Expected a non-empty value for `zoneid` but received {zoneid!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/dns/v1/records/{zoneid}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_service_health(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Get Service Health"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/dns/v1/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_service_metrics(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Get Service Metrics"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/dns/v1/metrics",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def list_zones(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Get All Zones"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/dns/v1/zones",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.get_nameserver_ip = to_raw_response_wrapper(
            v1.get_nameserver_ip,
        )
        self.get_records = to_raw_response_wrapper(
            v1.get_records,
        )
        self.get_service_health = to_raw_response_wrapper(
            v1.get_service_health,
        )
        self.get_service_metrics = to_raw_response_wrapper(
            v1.get_service_metrics,
        )
        self.list_zones = to_raw_response_wrapper(
            v1.list_zones,
        )

    @cached_property
    def zone(self) -> ZoneResourceWithRawResponse:
        return ZoneResourceWithRawResponse(self._v1.zone)

    @cached_property
    def record(self) -> RecordResourceWithRawResponse:
        return RecordResourceWithRawResponse(self._v1.record)


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.get_nameserver_ip = async_to_raw_response_wrapper(
            v1.get_nameserver_ip,
        )
        self.get_records = async_to_raw_response_wrapper(
            v1.get_records,
        )
        self.get_service_health = async_to_raw_response_wrapper(
            v1.get_service_health,
        )
        self.get_service_metrics = async_to_raw_response_wrapper(
            v1.get_service_metrics,
        )
        self.list_zones = async_to_raw_response_wrapper(
            v1.list_zones,
        )

    @cached_property
    def zone(self) -> AsyncZoneResourceWithRawResponse:
        return AsyncZoneResourceWithRawResponse(self._v1.zone)

    @cached_property
    def record(self) -> AsyncRecordResourceWithRawResponse:
        return AsyncRecordResourceWithRawResponse(self._v1.record)


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.get_nameserver_ip = to_streamed_response_wrapper(
            v1.get_nameserver_ip,
        )
        self.get_records = to_streamed_response_wrapper(
            v1.get_records,
        )
        self.get_service_health = to_streamed_response_wrapper(
            v1.get_service_health,
        )
        self.get_service_metrics = to_streamed_response_wrapper(
            v1.get_service_metrics,
        )
        self.list_zones = to_streamed_response_wrapper(
            v1.list_zones,
        )

    @cached_property
    def zone(self) -> ZoneResourceWithStreamingResponse:
        return ZoneResourceWithStreamingResponse(self._v1.zone)

    @cached_property
    def record(self) -> RecordResourceWithStreamingResponse:
        return RecordResourceWithStreamingResponse(self._v1.record)


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.get_nameserver_ip = async_to_streamed_response_wrapper(
            v1.get_nameserver_ip,
        )
        self.get_records = async_to_streamed_response_wrapper(
            v1.get_records,
        )
        self.get_service_health = async_to_streamed_response_wrapper(
            v1.get_service_health,
        )
        self.get_service_metrics = async_to_streamed_response_wrapper(
            v1.get_service_metrics,
        )
        self.list_zones = async_to_streamed_response_wrapper(
            v1.list_zones,
        )

    @cached_property
    def zone(self) -> AsyncZoneResourceWithStreamingResponse:
        return AsyncZoneResourceWithStreamingResponse(self._v1.zone)

    @cached_property
    def record(self) -> AsyncRecordResourceWithStreamingResponse:
        return AsyncRecordResourceWithStreamingResponse(self._v1.record)
