from __future__ import annotations

import httpx

from .asgV1 import (
    V1Resource,
    AsyncV1Resource,
    V1ResourceWithRawResponse,
    AsyncV1ResourceWithRawResponse,
    V1ResourceWithStreamingResponse,
    AsyncV1ResourceWithStreamingResponse,
)
from ...types import asg_get_asg_krn_by_vpc_params
from ..._types import Body, Query, Headers, NoneType, NotGiven, NOT_GIVEN
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["AsgResource", "AsyncAsgResource"]


class AsgResource(SyncAPIResource):
    @cached_property
    def v1(self) -> V1Resource:
        return V1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsgResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/asg-python#accessing-raw-response-data-eg-headers
        """
        return AsgResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsgResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/asg-python#with_streaming_response
        """
        return AsgResourceWithStreamingResponse(self)

    def get_asg_krn_by_vpc(
        self,
        *,
        page: int,
        size: int,
        vpc_krn: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get ASG KRN by VPC

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/v1/asg/get_asg_krn",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "size": size,
                        "vpc_krn": vpc_krn,
                    },
                    asg_get_asg_krn_by_vpc_params.AsgGetAsgKrnByVpcParams,
                ),
            ),
            cast_to=NoneType,
        )


class AsyncAsgResource(AsyncAPIResource):
    @cached_property
    def v1(self) -> AsyncV1Resource:
        return AsyncV1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAsgResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/asg-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAsgResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAsgResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/asg-python#with_streaming_response
        """
        return AsyncAsgResourceWithStreamingResponse(self)

    async def get_asg_krn_by_vpc(
        self,
        *,
        page: int,
        size: int,
        vpc_krn: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get ASG KRN by VPC

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/v1/asg/get_asg_krn",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "page": page,
                        "size": size,
                        "vpc_krn": vpc_krn,
                    },
                    asg_get_asg_krn_by_vpc_params.AsgGetAsgKrnByVpcParams,
                ),
            ),
            cast_to=NoneType,
        )


class AsgResourceWithRawResponse:
    def __init__(self, asg: AsgResource) -> None:
        self._asg = asg

        self.get_asg_krn_by_vpc = to_raw_response_wrapper(
            asg.get_asg_krn_by_vpc,
        )

    @cached_property
    def v1(self) -> V1ResourceWithRawResponse:
        return V1ResourceWithRawResponse(self._asg.v1)


class AsyncAsgResourceWithRawResponse:
    def __init__(self, asg: AsyncAsgResource) -> None:
        self._asg = asg

        self.get_asg_krn_by_vpc = async_to_raw_response_wrapper(
            asg.get_asg_krn_by_vpc,
        )

    @cached_property
    def v1(self) -> AsyncV1ResourceWithRawResponse:
        return AsyncV1ResourceWithRawResponse(self._asg.v1)


class AsgResourceWithStreamingResponse:
    def __init__(self, asg: AsgResource) -> None:
        self._asg = asg

        self.get_asg_krn_by_vpc = to_streamed_response_wrapper(
            asg.get_asg_krn_by_vpc,
        )

    @cached_property
    def v1(self) -> V1ResourceWithStreamingResponse:
        return V1ResourceWithStreamingResponse(self._asg.v1)


class AsyncAsgResourceWithStreamingResponse:
    def __init__(self, asg: AsyncAsgResource) -> None:
        self._asg = asg

        self.get_asg_krn_by_vpc = async_to_streamed_response_wrapper(
            asg.get_asg_krn_by_vpc,
        )

    @cached_property
    def v1(self) -> AsyncV1ResourceWithStreamingResponse:
        return AsyncV1ResourceWithStreamingResponse(self._asg.v1)