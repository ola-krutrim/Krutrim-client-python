# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx
import json
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
from ....types.dns.v1.zone import vpc_add_params, vpc_remove_params

__all__ = ["VpcResource", "AsyncVpcResource"]


class VpcResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VpcResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#accessing-raw-response-data-eg-headers
        """
        return VpcResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VpcResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#with_streaming_response
        """
        return VpcResourceWithStreamingResponse(self)

    def add(
        self,
        zoneid: str,
        *,
        vpcinfo: list[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Add VPC to Private Zone

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zoneid:
            raise ValueError(f"Expected a non-empty value for `zoneid` but received {zoneid!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/dns/v1/zone/{zoneid}/vpc",
            body=maybe_transform({"vpcinfo": vpcinfo}, vpc_add_params.VpcAddParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def remove(
        self,
        zoneid: str,
        *,
        vpcinfo: list[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Remove VPC from Private Zone

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
            f"/dns/v1/zone/{zoneid}/vpc",
            body=maybe_transform({"vpcinfo": vpcinfo}, vpc_remove_params.VpcRemoveParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncVpcResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVpcResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVpcResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVpcResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#with_streaming_response
        """
        return AsyncVpcResourceWithStreamingResponse(self)

    async def add(
        self,
        zoneid: str,
        *,
        vpcinfo: list[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Add VPC to Private Zone

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zoneid:
            raise ValueError(f"Expected a non-empty value for `zoneid` but received {zoneid!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/dns/v1/zone/{zoneid}/vpc",
            body=await async_maybe_transform({"vpcinfo": vpcinfo}, vpc_add_params.VpcAddParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def remove(
        self,
        zoneid: str,
        *,
        vpcinfo: list[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Remove VPC from Private Zone

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
            f"/dns/v1/zone/{zoneid}/vpc",
            body=await async_maybe_transform({"vpcinfo": vpcinfo}, vpc_remove_params.VpcRemoveParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class VpcResourceWithRawResponse:
    def __init__(self, vpc: VpcResource) -> None:
        self._vpc = vpc

        self.add = to_raw_response_wrapper(
            vpc.add,
        )
        self.remove = to_raw_response_wrapper(
            vpc.remove,
        )


class AsyncVpcResourceWithRawResponse:
    def __init__(self, vpc: AsyncVpcResource) -> None:
        self._vpc = vpc

        self.add = async_to_raw_response_wrapper(
            vpc.add,
        )
        self.remove = async_to_raw_response_wrapper(
            vpc.remove,
        )


class VpcResourceWithStreamingResponse:
    def __init__(self, vpc: VpcResource) -> None:
        self._vpc = vpc

        self.add = to_streamed_response_wrapper(
            vpc.add,
        )
        self.remove = to_streamed_response_wrapper(
            vpc.remove,
        )


class AsyncVpcResourceWithStreamingResponse:
    def __init__(self, vpc: AsyncVpcResource) -> None:
        self._vpc = vpc

        self.add = async_to_streamed_response_wrapper(
            vpc.add,
        )
        self.remove = async_to_streamed_response_wrapper(
            vpc.remove,
        )
