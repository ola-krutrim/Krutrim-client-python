# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from .vpc import (
    VpcResource,
    AsyncVpcResource,
    VpcResourceWithRawResponse,
    AsyncVpcResourceWithRawResponse,
    VpcResourceWithStreamingResponse,
    AsyncVpcResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, NOT_GIVEN
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.dns.v1 import zone_create_params

__all__ = ["ZoneResource", "AsyncZoneResource"]


class ZoneResource(SyncAPIResource):
    @cached_property
    def vpc(self) -> VpcResource:
        return VpcResource(self._client)

    @cached_property
    def with_raw_response(self) -> ZoneResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#accessing-raw-response-data-eg-headers
        """
        return ZoneResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ZoneResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#with_streaming_response
        """
        return ZoneResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        subnetid: str | Omit = omit,
        type: Literal["public", "private"] | Omit = omit,
        vpcid: str | Omit = omit,
        zonename: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Public or Private Zone

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/dns/v1/zone",
            body=maybe_transform(
                {
                    "subnetid": subnetid,
                    "type": type,
                    "vpcid": vpcid,
                    "zonename": zonename,
                },
                zone_create_params.ZoneCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def delete(
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
        Delete Zone

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zoneid:
            raise ValueError(f"Expected a non-empty value for `zoneid` but received {zoneid!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/dns/v1/zone/{zoneid}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )
    def fetch(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/dns/v1/zones",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )
    

    def fetchZoneById(
        self,
        zoneid:str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/dns/v1/zone/{zoneid}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

class AsyncZoneResource(AsyncAPIResource):
    @cached_property
    def vpc(self) -> AsyncVpcResource:
        return AsyncVpcResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncZoneResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#accessing-raw-response-data-eg-headers
        """
        return AsyncZoneResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncZoneResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#with_streaming_response
        """
        return AsyncZoneResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        subnetid: str | Omit = omit,
        type: Literal["public", "private"] | Omit = omit,
        vpcid: str | Omit = omit,
        zonename: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Public or Private Zone

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/dns/v1/zone",
            body=await async_maybe_transform(
                {
                    "subnetid": subnetid,
                    "type": type,
                    "vpcid": vpcid,
                    "zonename": zonename,
                },
                zone_create_params.ZoneCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def delete(
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
        Delete Zone

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zoneid:
            raise ValueError(f"Expected a non-empty value for `zoneid` but received {zoneid!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/dns/v1/zone/{zoneid}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )
    async def fetch(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/dns/v1/zones",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )
    

    async def fetchZoneById(
        self,
        zoneid:str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/dns/v1/zone/{zoneid}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

class ZoneResourceWithRawResponse:
    def __init__(self, zone: ZoneResource) -> None:
        self._zone = zone

        self.create = to_raw_response_wrapper(
            zone.create,
        )
        self.delete = to_raw_response_wrapper(
            zone.delete,
        )
        self.fetch = to_raw_response_wrapper(
            zone.fetch,
        )
        self.fetchZoneById = to_raw_response_wrapper(
            zone.fetchZoneById,
        )
    @cached_property
    def vpc(self) -> VpcResourceWithRawResponse:
        return VpcResourceWithRawResponse(self._zone.vpc)


class AsyncZoneResourceWithRawResponse:
    def __init__(self, zone: AsyncZoneResource) -> None:
        self._zone = zone

        self.create = async_to_raw_response_wrapper(
            zone.create,
        )
        self.delete = async_to_raw_response_wrapper(
            zone.delete,
        )
        self.fetch = async_to_raw_response_wrapper(
            zone.fetch,
        )
        self.fetchZoneById = async_to_raw_response_wrapper(
            zone.fetchZoneById,
        )
    @cached_property
    def vpc(self) -> AsyncVpcResourceWithRawResponse:
        return AsyncVpcResourceWithRawResponse(self._zone.vpc)


class ZoneResourceWithStreamingResponse:
    def __init__(self, zone: ZoneResource) -> None:
        self._zone = zone

        self.create = to_streamed_response_wrapper(
            zone.create,
        )
        self.delete = to_streamed_response_wrapper(
            zone.delete,
        )
        self.fetch = to_streamed_response_wrapper(
            zone.fetch,
        )
        self.fetchZoneById = to_streamed_response_wrapper(
            zone.fetchZoneById,
        )
    @cached_property
    def vpc(self) -> VpcResourceWithStreamingResponse:
        return VpcResourceWithStreamingResponse(self._zone.vpc)


class AsyncZoneResourceWithStreamingResponse:
    def __init__(self, zone: AsyncZoneResource) -> None:
        self._zone = zone

        self.create = async_to_streamed_response_wrapper(
            zone.create,
        )
        self.delete = async_to_streamed_response_wrapper(
            zone.delete,
        )
        self.fetch = async_to_streamed_response_wrapper(
            zone.fetch,
        )
        self.fetchZoneById = async_to_streamed_response_wrapper(
            zone.fetchZoneById,
        )
    @cached_property
    def vpc(self) -> AsyncVpcResourceWithStreamingResponse:
        return AsyncVpcResourceWithStreamingResponse(self._zone.vpc)
