from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx

from ..._types import NOT_GIVEN, Query, Headers, NotGiven
from ._helpers import validate_identifier, normalize_proxy_content
from ..._compat import cached_property
from ..._models import FinalRequestOptions
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["ProxyResource", "AsyncProxyResource"]


_SUPPORTED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}


def _proxy_path(path: str) -> str:
    normalized = path.lstrip("/")
    if any(segment == ".." for segment in normalized.split("/")):
        raise ValueError("proxy path cannot contain traversal segments")
    return quote(normalized, safe="/!$&'()*+,-.:;=@_~")


class ProxyResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProxyResourceWithRawResponse:
        return ProxyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProxyResourceWithStreamingResponse:
        return ProxyResourceWithStreamingResponse(self)

    def request(
        self,
        sandbox_id: str,
        method: str,
        path: str,
        *,
        query: Query | None = None,
        headers: Headers | None = None,
        json: Any = None,
        content: str | bytes | None = None,
        max_retries: int = 0,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> bytes:
        validate_identifier(sandbox_id)
        normalized_method = method.upper()
        if normalized_method not in _SUPPORTED_METHODS:
            raise ValueError(f"unsupported proxy HTTP method: {method}")
        if json is not None and content is not None:
            raise ValueError("proxy json and raw content are mutually exclusive")
        proxy_path = _proxy_path(path)
        raw_content = normalize_proxy_content(content)
        merged_headers = {**(headers or {}), **(extra_headers or {})}
        merged_query = {**(query or {}), **(extra_query or {})}
        request_options = make_request_options(query=merged_query, extra_headers=merged_headers, timeout=timeout)
        request_options["max_retries"] = max_retries
        options = FinalRequestOptions.construct(
            method=normalized_method,
            url=f"/omni/sandbox/v1/{sandbox_id}/{proxy_path}",
            json_data=json,
            content=raw_content,
            **request_options,
        )
        return self._client.request(bytes, options)


class AsyncProxyResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProxyResourceWithRawResponse:
        return AsyncProxyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProxyResourceWithStreamingResponse:
        return AsyncProxyResourceWithStreamingResponse(self)

    async def request(
        self,
        sandbox_id: str,
        method: str,
        path: str,
        *,
        query: Query | None = None,
        headers: Headers | None = None,
        json: Any = None,
        content: str | bytes | None = None,
        max_retries: int = 0,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> bytes:
        validate_identifier(sandbox_id)
        normalized_method = method.upper()
        if normalized_method not in _SUPPORTED_METHODS:
            raise ValueError(f"unsupported proxy HTTP method: {method}")
        if json is not None and content is not None:
            raise ValueError("proxy json and raw content are mutually exclusive")
        proxy_path = _proxy_path(path)
        raw_content = normalize_proxy_content(content)
        merged_headers = {**(headers or {}), **(extra_headers or {})}
        merged_query = {**(query or {}), **(extra_query or {})}
        request_options = make_request_options(query=merged_query, extra_headers=merged_headers, timeout=timeout)
        request_options["max_retries"] = max_retries
        options = FinalRequestOptions.construct(
            method=normalized_method,
            url=f"/omni/sandbox/v1/{sandbox_id}/{proxy_path}",
            json_data=json,
            content=raw_content,
            **request_options,
        )
        return await self._client.request(bytes, options)


class ProxyResourceWithRawResponse:
    def __init__(self, proxy: ProxyResource) -> None:
        self.request = to_custom_raw_response_wrapper(proxy.request, BinaryAPIResponse)


class AsyncProxyResourceWithRawResponse:
    def __init__(self, proxy: AsyncProxyResource) -> None:
        self.request = async_to_custom_raw_response_wrapper(proxy.request, AsyncBinaryAPIResponse)


class ProxyResourceWithStreamingResponse:
    def __init__(self, proxy: ProxyResource) -> None:
        self.request = to_custom_streamed_response_wrapper(proxy.request, StreamedBinaryAPIResponse)


class AsyncProxyResourceWithStreamingResponse:
    def __init__(self, proxy: AsyncProxyResource) -> None:
        self.request = async_to_custom_streamed_response_wrapper(proxy.request, AsyncStreamedBinaryAPIResponse)
