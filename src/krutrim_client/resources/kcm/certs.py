# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Mapping, cast

import httpx

from .tags import (
    TagsResource,
    AsyncTagsResource,
    TagsResourceWithRawResponse,
    AsyncTagsResourceWithRawResponse,
    TagsResourceWithStreamingResponse,
    AsyncTagsResourceWithStreamingResponse,
)
from ...types.kcm import (
    cert_list_params,
    cert_import_params,
    cert_update_params,
    cert_retrieve_params,
    cert_get_expiring_params,
)
from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, FileTypes, omit, NOT_GIVEN
from ..._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["CertsResource", "AsyncCertsResource"]


class CertsResource(SyncAPIResource):
    @cached_property
    def tags(self) -> TagsResource:
        return TagsResource(self._client)

    @cached_property
    def with_raw_response(self) -> CertsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/kcm1-python#accessing-raw-response-data-eg-headers
        """
        return CertsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CertsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/kcm1-python#with_streaming_response
        """
        return CertsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        cert_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """3.

        Get Certificate by ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """

        if not cert_id:
            raise ValueError(f"Expected a non-empty value for `cert_id` but received {cert_id!r}")
        
        extra_query = {
                "certId": cert_id,
                **(extra_query or {})
            }

        return self._get(
            "/kcm/v1/certs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=NoneType,
        )

    def update(
        self,
        path_cert_id: str,
        *,
        x_vpc_id: str,
        cert_file: FileTypes | Omit = omit,
        flag: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """8.

        Update Certificate Bundle (Binary)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_cert_id:
            raise ValueError(f"Expected a non-empty value for `path_cert_id` but received {path_cert_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"X-Vpc-Id": x_vpc_id})
        body = deepcopy_minimal(
            {
                "cert_file": cert_file,
                "flag": flag,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["certFile"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers["Content-Type"] = "multipart/form-data"
        return self._put(
            f"/certs/update/{path_cert_id}",
            body=maybe_transform(body, cert_update_params.CertUpdateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list(
        self,
        *,
        vpc_id: str,
        # lbtype: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """2.

        List Certificates

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/kcm/v1/certs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "vpcId": vpc_id
                    },
                    cert_list_params.CertListParams,
                ),
            ),
            cast_to=NoneType,
        )

    def delete(
        self,
        path_cert_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """4.

        Delete Certificate

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_cert_id:
            raise ValueError(f"Expected a non-empty value for `path_cert_id` but received {path_cert_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/kcm/v1/certs/{path_cert_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get_expiring(
        self,
        *,
        date: str,
        vpc_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """5.

        Get Expiring Certificates

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "kcm/v1/certs/expiringIn",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "date": date,
                        "vpc_id": vpc_id,
                    },
                    cert_get_expiring_params.CertGetExpiringParams,
                ),
            ),
            cast_to=NoneType,
        )

    def import_file(
        self,
        *,
        cert_file: FileTypes | Omit = omit,
        vpc_id:str,
        flag: str | Omit = omit,
        name: str | Omit = omit,
        tags: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        extra_headers = {"Accept": "*/*","X-Vpc-Id": vpc_id, **(extra_headers or {})}

        from os import PathLike
        if cert_file is not omit and isinstance(cert_file, (str, PathLike)):
            cert_file = open(str(cert_file), "rb")

        body = deepcopy_minimal(
            {
                "certFile": cert_file,
                "flag": flag,
                "name": name,
                "tags": tags,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["certFile"]])
        extra_headers["Content-Type"] = "multipart/form-data"
        return self._post(
            "/kcm/v1/certs/import",
            body=maybe_transform(body, cert_import_params.CertImportParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=NoneType,
        )



class AsyncCertsResource(AsyncAPIResource):
    @cached_property
    def tags(self) -> AsyncTagsResource:
        return AsyncTagsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCertsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/kcm1-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCertsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCertsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/kcm1-python#with_streaming_response
        """
        return AsyncCertsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        cert_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """3.

        Get Certificate by ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        if not cert_id:
           raise ValueError(f"Expected a non-empty value for `cert_id` but received {cert_id!r}")
        
        extra_query = {
                "certId": cert_id,
                **(extra_query or {})
            }

        return await self._get(
            "/kcm/v1/certs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=NoneType,
        )

    async def update(
        self,
        path_cert_id: str,
        *,
        x_vpc_id: str,
        cert_file: FileTypes | Omit = omit,
        flag: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """8.

        Update Certificate Bundle (Binary)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_cert_id:
            raise ValueError(f"Expected a non-empty value for `path_cert_id` but received {path_cert_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"X-Vpc-Id": x_vpc_id})
        body = deepcopy_minimal(
            {
                "cert_file": cert_file,
                "flag": flag,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["certFile"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers["Content-Type"] = "multipart/form-data"
        return await self._put(
            f"/certs/update/{path_cert_id}",
            body=await async_maybe_transform(body, cert_update_params.CertUpdateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def list(
        self,
        *,
        vpc_id: str,
        lbtype: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """2.

        List Certificates

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/kcm/v1/certs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "vpc_id": vpc_id,
                        "lbtype": lbtype,
                    },
                    cert_list_params.CertListParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def delete(
        self,
        path_cert_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """4.

        Delete Certificate

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_cert_id:
            raise ValueError(f"Expected a non-empty value for `path_cert_id` but received {path_cert_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/kcm/v1/certs/{path_cert_id}{path_cert_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_expiring(
        self,
        *,
        date: str,
        vpc_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """5.

        Get Expiring Certificates

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "kcm/v1/certs/expiringIn",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "date": date,
                        "vpc_id": vpc_id,
                    },
                    cert_get_expiring_params.CertGetExpiringParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def import_file(
        self,
        *,
        cert_file: FileTypes | Omit = omit,
        flag: str | Omit = omit,
        name: str | Omit = omit,
        tags: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:

        extra_headers = {"Accept": "*/*", **(extra_headers or {})}

        body = deepcopy_minimal(
            {
                "certFile": cert_file,   
                "flag": flag,
                "name": name,
                "tags": tags,
            }
        )

        files = extract_files(
            cast(Mapping[str, object], body),
            paths=[["certFile"]]       
        )
        extra_headers["Content-Type"] = "multipart/form-data"
        return await self._post(
            "/kcm/v1/certs/import",
            body=await async_maybe_transform(body, cert_import_params.CertImportParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=NoneType,
        )



class CertsResourceWithRawResponse:
    def __init__(self, certs: CertsResource) -> None:
        self._certs = certs

        self.retrieve = to_raw_response_wrapper(
            certs.retrieve,
        )
        self.update = to_raw_response_wrapper(
            certs.update,
        )
        self.list = to_raw_response_wrapper(
            certs.list,
        )
        self.delete = to_raw_response_wrapper(
            certs.delete,
        )
        self.get_expiring = to_raw_response_wrapper(
            certs.get_expiring,
        )
        self.import_file = to_raw_response_wrapper(
            certs.import_file,
        )

    @cached_property
    def tags(self) -> TagsResourceWithRawResponse:
        return TagsResourceWithRawResponse(self._certs.tags)


class AsyncCertsResourceWithRawResponse:
    def __init__(self, certs: AsyncCertsResource) -> None:
        self._certs = certs

        self.retrieve = async_to_raw_response_wrapper(
            certs.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            certs.update,
        )
        self.list = async_to_raw_response_wrapper(
            certs.list,
        )
        self.delete = async_to_raw_response_wrapper(
            certs.delete,
        )
        self.get_expiring = async_to_raw_response_wrapper(
            certs.get_expiring,
        )
        self.import_file = async_to_raw_response_wrapper(
            certs.import_file,
        )

    @cached_property
    def tags(self) -> AsyncTagsResourceWithRawResponse:
        return AsyncTagsResourceWithRawResponse(self._certs.tags)


class CertsResourceWithStreamingResponse:
    def __init__(self, certs: CertsResource) -> None:
        self._certs = certs

        self.retrieve = to_streamed_response_wrapper(
            certs.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            certs.update,
        )
        self.list = to_streamed_response_wrapper(
            certs.list,
        )
        self.delete = to_streamed_response_wrapper(
            certs.delete,
        )
        self.get_expiring = to_streamed_response_wrapper(
            certs.get_expiring,
        )
        self.import_file = to_streamed_response_wrapper(
            certs.import_file,
        )

    @cached_property
    def tags(self) -> TagsResourceWithStreamingResponse:
        return TagsResourceWithStreamingResponse(self._certs.tags)


class AsyncCertsResourceWithStreamingResponse:
    def __init__(self, certs: AsyncCertsResource) -> None:
        self._certs = certs

        self.retrieve = async_to_streamed_response_wrapper(
            certs.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            certs.update,
        )
        self.list = async_to_streamed_response_wrapper(
            certs.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            certs.delete,
        )
        self.get_expiring = async_to_streamed_response_wrapper(
            certs.get_expiring,
        )
        self.import_file = async_to_streamed_response_wrapper(
            certs.import_file,
        )

    @cached_property
    def tags(self) -> AsyncTagsResourceWithStreamingResponse:
        return AsyncTagsResourceWithStreamingResponse(self._certs.tags)