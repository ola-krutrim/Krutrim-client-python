# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, NOT_GIVEN
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
from ...types.dns.v1 import record_create_params, record_update_params

__all__ = ["RecordResource", "AsyncRecordResource"]


class RecordResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RecordResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#accessing-raw-response-data-eg-headers
        """
        return RecordResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RecordResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#with_streaming_response
        """
        return RecordResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        krnid: str | Omit = omit,
        value: str,
        rname: str | Omit = omit,
        ttl: int | Omit = omit,
        TYPE: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Add DNS Record

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/dns/v1/record",
            body=maybe_transform(
                {
                    "krnid": krnid,
                    "records": [
                        {
                            "value":value
                        }
                    ],
                    "rname": rname,
                    "ttl": ttl,
                    "type": TYPE,
                },
                record_create_params.RecordCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def update(
        self,
        recordid: str,
        rname: str,
        *,
        records: Iterable[record_update_params.Record] | Omit = omit,
        value: str | Omit = omit,
        routing: str | Omit = omit,
        TYPE: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Update Record

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/dns/v1/record/{recordid}",
            body=maybe_transform(
                {
                    "records": [
                        {
                            "value":value
                        }
                    ],
                    "rname": rname,
                    "routing": routing,
                    "type": TYPE,
                },
                record_update_params.RecordUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def delete(
        self,
        recordid: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Record

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not recordid:
            raise ValueError(f"Expected a non-empty value for `recordid` but received {recordid!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/dns/v1/record/{recordid}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


    def fetchrecord(
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
        Delete Record

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

class AsyncRecordResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRecordResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRecordResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRecordResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/dns-6-python#with_streaming_response
        """
        return AsyncRecordResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        krnid: str | Omit = omit,
        value: str,
        rname: str | Omit = omit,
        routing: str | Omit = omit,
        ttl: int | Omit = omit,
        TYPE: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Add DNS Record

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/dns/v1/record",
            body=await async_maybe_transform(
                {
                    "krnid": krnid,
                    "records": [
                        {
                            "value":value
                        }
                    ],
                    "rname": rname,
                    "routing": routing,
                    "ttl": ttl,
                    "type": TYPE,
                },
                record_create_params.RecordCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def update(
        self,
        recordid: str,
        rname: str,
        *,
        records: Iterable[record_update_params.Record] | Omit = omit,
        value: str | Omit = omit,
        routing: str | Omit = omit,
        TYPE: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Update Record

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            f"/dns/v1/record/{recordid}",
            body=await async_maybe_transform(
                {
                    "records": records,
                    "rname": rname,
                    "routing": routing,
                    "type": TYPE,
                },
                record_update_params.RecordUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def delete(
        self,
        recordid: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Record

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not recordid:
            raise ValueError(f"Expected a non-empty value for `recordid` but received {recordid!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/dns/v1/record/{recordid}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )



    async def fetchrecord(
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
        Delete Record

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

class RecordResourceWithRawResponse:
    def __init__(self, record: RecordResource) -> None:
        self._record = record

        self.create = to_raw_response_wrapper(
            record.create,
        )
        self.update = to_raw_response_wrapper(
            record.update,
        )
        self.delete = to_raw_response_wrapper(
            record.delete,
        )
        self.fetchrecord = to_raw_response_wrapper(
            record.fetchrecord,
        )

class AsyncRecordResourceWithRawResponse:
    def __init__(self, record: AsyncRecordResource) -> None:
        self._record = record

        self.create = async_to_raw_response_wrapper(
            record.create,
        )
        self.update = async_to_raw_response_wrapper(
            record.update,
        )
        self.delete = async_to_raw_response_wrapper(
            record.delete,
        )
        self.fetchrecord = async_to_raw_response_wrapper(
            record.fetchrecord,
        )

class RecordResourceWithStreamingResponse:
    def __init__(self, record: RecordResource) -> None:
        self._record = record

        self.create = to_streamed_response_wrapper(
            record.create,
        )
        self.update = to_streamed_response_wrapper(
            record.update,
        )
        self.delete = to_streamed_response_wrapper(
            record.delete,
        )
        self.fetchrecord = to_streamed_response_wrapper(
            record.fetchrecord,
        )


class AsyncRecordResourceWithStreamingResponse:
    def __init__(self, record: AsyncRecordResource) -> None:
        self._record = record

        self.create = async_to_streamed_response_wrapper(
            record.create,
        )
        self.update = async_to_streamed_response_wrapper(
            record.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            record.delete,
        )
        self.fetchrecord = async_to_streamed_response_wrapper(
            record.fetchrecord,
        )
