# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from typing import Mapping, cast, Dict

from ..._types import Body, Omit, Query, Headers, NoneType, FileTypes, NotGiven, omit, NOT_GIVEN
from ..._utils import maybe_transform, async_maybe_transform, deepcopy_minimal, extract_files
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.kcm import tag_list_params, tag_update_params
from ..._base_client import make_request_options

__all__ = ["TagsResource", "AsyncTagsResource"]


class TagsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TagsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/kcm1-python#accessing-raw-response-data-eg-headers
        """
        return TagsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TagsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/kcm1-python#with_streaming_response
        """
        return TagsResourceWithStreamingResponse(self)

    def updateCertificate(
        self,
        *,
        path_cert_id: str,
        cert_file: FileTypes | Omit = omit,
        vpc_id: str,
        flag: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """6.

        Update Tags (JSON)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*","X-Vpc-Id": vpc_id, **(extra_headers or {})}

        from os import PathLike
        if cert_file is not omit and isinstance(cert_file, (str, PathLike)):
            cert_file = open(str(cert_file), "rb")

        body = deepcopy_minimal(
            {
                "certFile": cert_file,
                "flag": flag
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["certFile"]])
        extra_headers["Content-Type"] = "multipart/form-data"

        if not path_cert_id:
            raise ValueError(f"Expected a non-empty value for `path_cert_id` but received {path_cert_id!r}")
        return self._put(
            f"/kcm/v1/certs/{path_cert_id}",
            body=maybe_transform(body, tag_update_params.TagUpdateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )
    
    def addCertificateTag(
        self,
        *,
        path_cert_id: str,
        tags: Dict[str, str],
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """7.

        add tags (JSON)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        if not path_cert_id:
            raise ValueError(f"Expected a non-empty value for `path_cert_id` but received {path_cert_id!r}")

        return self._post(
            f"/kcm/v1/certs/tags/{path_cert_id}",
            body=tags,
            options=make_request_options(
                extra_headers=extra_headers,
                timeout=timeout,
            ),
            cast_to=None,
        )

    def getTagValue (
        self,
        *,
        cert_id: str,
        tag_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """8.

        Get Tag Value

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/kcm/v1/certs/tags",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cert_id": cert_id,
                        "tag_name": tag_name,
                    },
                    tag_list_params.TagListParams,
                ),
            ),
            cast_to=NoneType,
        )
    
    


class AsyncTagsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTagsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/kcm1-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTagsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTagsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/kcm1-python#with_streaming_response
        """
        return AsyncTagsResourceWithStreamingResponse(self)

    async def updateCertificate(
        self,
        *,
        path_cert_id: str,
        cert_file: FileTypes | Omit = omit,
        vpc_id: str,
        flag: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """6.

        Update Tags (JSON)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*","X-Vpc-Id": vpc_id, **(extra_headers or {})}

        from os import PathLike
        if cert_file is not omit and isinstance(cert_file, (str, PathLike)):
            cert_file = open(str(cert_file), "rb")

        body = deepcopy_minimal(
            {
                "certFile": cert_file,
                "flag": flag
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["certFile"]])
        extra_headers["Content-Type"] = "multipart/form-data"

        if not path_cert_id:
            raise ValueError(f"Expected a non-empty value for `path_cert_id` but received {path_cert_id!r}")
        return await self._put(
            f"/kcm/v1/certs/{path_cert_id}",
            body=await async_maybe_transform(body, tag_update_params.TagUpdateParams),
            files=files,
            options= make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )
    
    async def addCertificateTag(
        self,
        *,
        path_cert_id: str,
        tags: Dict[str, str],
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """7.

        add tags (JSON)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        if not path_cert_id:
            raise ValueError(f"Expected a non-empty value for `path_cert_id` but received {path_cert_id!r}")

        return await self._post(
            f"/kcm/v1/certs/tags/{path_cert_id}",
            body=tags,
            options=make_request_options(
                extra_headers=extra_headers,
                timeout=timeout,
            ),
            cast_to=None,
        )

    async def getTagValue(
        self,
        *,
        cert_id: str,
        tag_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """7.

        Get Tag Value

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/kcm/v1/certs/tags",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cert_id": cert_id,
                        "tag_name": tag_name,
                    },
                    tag_list_params.TagListParams,
                ),
            ),
            cast_to=NoneType,
        )


class TagsResourceWithRawResponse:
    def __init__(self, tags: TagsResource) -> None:
        self._tags = tags

        self.updateCertificate = to_raw_response_wrapper(
            tags.updateCertificate,
        )
        self.getTagValue = to_raw_response_wrapper(
            tags.getTagValue,
        )
        self.addCertificateTag = to_raw_response_wrapper(
            tags.addCertificateTag,
        )


class AsyncTagsResourceWithRawResponse:
    def __init__(self, tags: AsyncTagsResource) -> None:
        self._tags = tags

        self.updateCertificate = async_to_raw_response_wrapper(
            tags.updateCertificate,
        )
        self.getTagValue = async_to_raw_response_wrapper(
            tags.getTagValue,
        )
        self.addCertificateTag = async_to_raw_response_wrapper(
            tags.addCertificateTag,
        )


class TagsResourceWithStreamingResponse:
    def __init__(self, tags: TagsResource) -> None:
        self._tags = tags

        self.updateCertificate = to_streamed_response_wrapper(
            tags.updateCertificate,
        )
        self.getTagValue = to_streamed_response_wrapper(
            tags.getTagValue,
        )
        self.addCertificateTag = to_streamed_response_wrapper(
            tags.addCertificateTag,
        )


class AsyncTagsResourceWithStreamingResponse:
    def __init__(self, tags: AsyncTagsResource) -> None:
        self._tags = tags

        self.updateCertificate = async_to_streamed_response_wrapper(
            tags.updateCertificate,
        )
        self.getTagValue = async_to_streamed_response_wrapper(
            tags.getTagValue,
        )
        self.addCertificateTag = async_to_streamed_response_wrapper(
            tags.addCertificateTag,
        )