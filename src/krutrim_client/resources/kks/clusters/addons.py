# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

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
from ....types.kks.clusters import addon_install_params

__all__ = ["AddonsResource", "AsyncAddonsResource"]


class AddonsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AddonsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/kks-python#accessing-raw-response-data-eg-headers
        """
        return AddonsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AddonsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/kks-python#with_streaming_response
        """
        return AddonsResourceWithStreamingResponse(self)

    def list(
        self,
        cluster_krn: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        List Cluster Addons

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/v1/kks/clusters/{cluster_krn}/addons",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        List Cluster Addons

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/v1/kks/addons",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


    def delete(
        self,
        addon_krn: str,
        *,
        cluster_krn: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Addon

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        if not addon_krn:
            raise ValueError(f"Expected a non-empty value for `addon_krn` but received {addon_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/v1/kks/clusters/{cluster_krn}/addons/{addon_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def install(
        self,
        cluster_krn: str,
        *,
        addon_name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Install Addon

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/v1/kks/clusters/{cluster_krn}/addons",
            body=maybe_transform({"addon_name": addon_name}, addon_install_params.AddonInstallParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncAddonsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAddonsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/kks-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAddonsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAddonsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/kks-python#with_streaming_response
        """
        return AsyncAddonsResourceWithStreamingResponse(self)

    async def list(
        self,
        cluster_krn: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        List Cluster Addons

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/v1/kks/clusters/{cluster_krn}/addons",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        List Cluster Addons

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/v1/kks/addons",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


    async def delete(
        self,
        addon_krn: str,
        *,
        cluster_krn: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Addon

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        if not addon_krn:
            raise ValueError(f"Expected a non-empty value for `addon_krn` but received {addon_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/v1/kks/clusters/{cluster_krn}/addons/{addon_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def install(
        self,
        cluster_krn: str,
        *,
        addon_name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Install Addon

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/v1/kks/clusters/{cluster_krn}/addons",
            body=await async_maybe_transform({"addon_name": addon_name}, addon_install_params.AddonInstallParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AddonsResourceWithRawResponse:
    def __init__(self, addons: AddonsResource) -> None:
        self._addons = addons

        self.list = to_raw_response_wrapper(
            addons.list,
        )
        self.delete = to_raw_response_wrapper(
            addons.delete,
        )
        self.install = to_raw_response_wrapper(
            addons.install,
        )
        self.retrieve = to_raw_response_wrapper(
            addons.retrieve,
        )


class AsyncAddonsResourceWithRawResponse:
    def __init__(self, addons: AsyncAddonsResource) -> None:
        self._addons = addons

        self.list = async_to_raw_response_wrapper(
            addons.list,
        )
        self.delete = async_to_raw_response_wrapper(
            addons.delete,
        )
        self.install = async_to_raw_response_wrapper(
            addons.install,
        )
        self.retrieve = async_to_raw_response_wrapper(
            addons.retrieve,
        )


class AddonsResourceWithStreamingResponse:
    def __init__(self, addons: AddonsResource) -> None:
        self._addons = addons

        self.list = to_streamed_response_wrapper(
            addons.list,
        )
        self.delete = to_streamed_response_wrapper(
            addons.delete,
        )
        self.install = to_streamed_response_wrapper(
            addons.install,
        )
        self.retrieve = to_streamed_response_wrapper(
            addons.retrieve,
        )


class AsyncAddonsResourceWithStreamingResponse:
    def __init__(self, addons: AsyncAddonsResource) -> None:
        self._addons = addons

        self.list = async_to_streamed_response_wrapper(
            addons.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            addons.delete,
        )
        self.install = async_to_streamed_response_wrapper(
            addons.install,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            addons.retrieve,
        )
