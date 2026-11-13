from __future__ import annotations

from typing import Iterable, AsyncIterable

import httpx

from ._common import PREFIX, prepare, identifier
from ..._types import NOT_GIVEN, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ...types.sandbox_service import (
    FileUploadResponse,
)


class FilesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FilesResourceWithRawResponse:
        return FilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FilesResourceWithStreamingResponse:
        return FilesResourceWithStreamingResponse(self)

    def upload(
        self,
        *,
        krn_id: str,
        x_region: str,
        content: bytes | Iterable[bytes],
        path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileUploadResponse:
        """PUT /sandbox/v1/sandboxes/{krn_id}/files. Sends raw bytes, with retries disabled. Parent directories must exist."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="files.upload",
            x_region=x_region,
            body={},
            query={"path": path},
            extra_headers={
                **{name: value for name, value in (extra_headers or {}).items() if name.lower() != "content-type"},
                "Content-Type": "application/octet-stream",
            },
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
            unsafe=True,
        )
        options["content"] = content
        return self._put(f"{PREFIX}/sandboxes/{krn_id}/files", cast_to=FileUploadResponse, options=options)

    def download(
        self,
        *,
        krn_id: str,
        x_region: str,
        path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/files. Returns a binary response; use with_streaming_response for large files."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="files.download",
            x_region=x_region,
            body={},
            query={"path": path},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(f"{PREFIX}/sandboxes/{krn_id}/files", cast_to=BinaryAPIResponse, options=options)


class AsyncFilesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFilesResourceWithRawResponse:
        return AsyncFilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFilesResourceWithStreamingResponse:
        return AsyncFilesResourceWithStreamingResponse(self)

    async def upload(
        self,
        *,
        krn_id: str,
        x_region: str,
        content: bytes | AsyncIterable[bytes],
        path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileUploadResponse:
        """PUT /sandbox/v1/sandboxes/{krn_id}/files. Sends raw bytes, with retries disabled. Parent directories must exist."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="files.upload",
            x_region=x_region,
            body={},
            query={"path": path},
            extra_headers={
                **{name: value for name, value in (extra_headers or {}).items() if name.lower() != "content-type"},
                "Content-Type": "application/octet-stream",
            },
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
            unsafe=True,
        )
        options["content"] = content
        return await self._put(f"{PREFIX}/sandboxes/{krn_id}/files", cast_to=FileUploadResponse, options=options)

    async def download(
        self,
        *,
        krn_id: str,
        x_region: str,
        path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/files. Returns a binary response; use with_streaming_response for large files."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="files.download",
            x_region=x_region,
            body={},
            query={"path": path},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(f"{PREFIX}/sandboxes/{krn_id}/files", cast_to=AsyncBinaryAPIResponse, options=options)


class FilesResourceWithRawResponse:
    def __init__(self, resource: FilesResource) -> None:
        self.upload = to_raw_response_wrapper(resource.upload)
        self.download = to_raw_response_wrapper(resource.download)


class FilesResourceWithStreamingResponse:
    def __init__(self, resource: FilesResource) -> None:
        self.upload = to_streamed_response_wrapper(resource.upload)
        self.download = to_custom_streamed_response_wrapper(resource.download, StreamedBinaryAPIResponse)


class AsyncFilesResourceWithRawResponse:
    def __init__(self, resource: AsyncFilesResource) -> None:
        self.upload = async_to_raw_response_wrapper(resource.upload)
        self.download = async_to_raw_response_wrapper(resource.download)


class AsyncFilesResourceWithStreamingResponse:
    def __init__(self, resource: AsyncFilesResource) -> None:
        self.upload = async_to_streamed_response_wrapper(resource.upload)
        self.download = async_to_custom_streamed_response_wrapper(resource.download, AsyncStreamedBinaryAPIResponse)
