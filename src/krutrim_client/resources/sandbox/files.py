from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ._helpers import (
    validate_identifier,
    normalize_file_content,
    validate_required_path,
    normalize_file_content_async,
)
from ..._compat import cached_property
from ..._models import FinalRequestOptions
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.sandbox import (
    SandboxFileContent,
    SandboxFileResponse,
    SandboxEntryResponse,
    SandboxEntryListResponse,
)

__all__ = ["FilesResource", "AsyncFilesResource"]


class FilesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FilesResourceWithRawResponse:
        return FilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FilesResourceWithStreamingResponse:
        return FilesResourceWithStreamingResponse(self)

    def upload(
        self,
        sandbox_id: str,
        *,
        path: str,
        content: SandboxFileContent,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxFileResponse:
        validate_identifier(sandbox_id)
        validate_required_path(path)
        raw_content = normalize_file_content(content)
        headers = {"Accept": "application/json", "Content-Type": "application/octet-stream", **(extra_headers or {})}
        query = {"path": path, **(extra_query or {})}
        request_options = make_request_options(query=query, extra_headers=headers, timeout=timeout)
        options = FinalRequestOptions.construct(
            method="post",
            url=f"/omni/sandbox/v1/sandbox/{sandbox_id}/files",
            content=raw_content,
            **request_options,
        )
        return self._client.request(SandboxFileResponse, options)

    def download(
        self,
        sandbox_id: str,
        *,
        path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> bytes:
        validate_identifier(sandbox_id)
        validate_required_path(path)
        return self._get(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/files",
            cast_to=bytes,
            options=make_request_options(
                query={"path": path},
                extra_headers={"Accept": "application/octet-stream", **(extra_headers or {})},
                extra_query=extra_query,
                timeout=timeout,
            ),
        )

    def delete(
        self,
        sandbox_id: str,
        *,
        path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxFileResponse:
        validate_identifier(sandbox_id)
        validate_required_path(path)
        return self._delete(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/files",
            cast_to=SandboxFileResponse,
            options=make_request_options(
                query={"path": path},
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    def list(
        self,
        sandbox_id: str,
        *,
        path: str | None = None,
        depth: int | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxEntryListResponse:
        validate_identifier(sandbox_id)
        if depth is not None and not 1 <= depth <= 10:
            raise ValueError("depth must be between 1 and 10")
        query: dict[str, object] = {}
        if path is not None:
            query["path"] = path
        if depth is not None:
            query["depth"] = depth
        return self._get(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/files/list",
            cast_to=SandboxEntryListResponse,
            options=make_request_options(
                query=query, extra_headers=extra_headers, extra_query=extra_query, timeout=timeout
            ),
        )

    def stat(
        self,
        sandbox_id: str,
        *,
        path: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxEntryResponse:
        validate_identifier(sandbox_id)
        query: dict[str, object] = {}
        if path is not None:
            query["path"] = path
        return self._get(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/files/stat",
            cast_to=SandboxEntryResponse,
            options=make_request_options(
                query=query, extra_headers=extra_headers, extra_query=extra_query, timeout=timeout
            ),
        )

    def move(
        self,
        sandbox_id: str,
        *,
        path: str,
        new_path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxFileResponse:
        validate_identifier(sandbox_id)
        validate_required_path(path)
        validate_required_path(new_path)
        return self._put(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/files/move",
            cast_to=SandboxFileResponse,
            options=make_request_options(
                query={"path": path, "newPath": new_path},
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    def make_directory(
        self,
        sandbox_id: str,
        *,
        path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxFileResponse:
        validate_identifier(sandbox_id)
        validate_required_path(path)
        return self._post(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/dirs",
            cast_to=SandboxFileResponse,
            options=make_request_options(
                query={"path": path},
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )


class AsyncFilesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFilesResourceWithRawResponse:
        return AsyncFilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFilesResourceWithStreamingResponse:
        return AsyncFilesResourceWithStreamingResponse(self)

    async def upload(
        self,
        sandbox_id: str,
        *,
        path: str,
        content: SandboxFileContent,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxFileResponse:
        validate_identifier(sandbox_id)
        validate_required_path(path)
        raw_content = await normalize_file_content_async(content)
        headers = {"Accept": "application/json", "Content-Type": "application/octet-stream", **(extra_headers or {})}
        query = {"path": path, **(extra_query or {})}
        request_options = make_request_options(query=query, extra_headers=headers, timeout=timeout)
        options = FinalRequestOptions.construct(
            method="post",
            url=f"/omni/sandbox/v1/sandbox/{sandbox_id}/files",
            content=raw_content,
            **request_options,
        )
        return await self._client.request(SandboxFileResponse, options)

    async def download(
        self,
        sandbox_id: str,
        *,
        path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> bytes:
        validate_identifier(sandbox_id)
        validate_required_path(path)
        return await self._get(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/files",
            cast_to=bytes,
            options=make_request_options(
                query={"path": path},
                extra_headers={"Accept": "application/octet-stream", **(extra_headers or {})},
                extra_query=extra_query,
                timeout=timeout,
            ),
        )

    async def delete(
        self,
        sandbox_id: str,
        *,
        path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxFileResponse:
        validate_identifier(sandbox_id)
        validate_required_path(path)
        return await self._delete(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/files",
            cast_to=SandboxFileResponse,
            options=make_request_options(
                query={"path": path},
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    async def list(
        self,
        sandbox_id: str,
        *,
        path: str | None = None,
        depth: int | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxEntryListResponse:
        validate_identifier(sandbox_id)
        if depth is not None and not 1 <= depth <= 10:
            raise ValueError("depth must be between 1 and 10")
        query: dict[str, object] = {}
        if path is not None:
            query["path"] = path
        if depth is not None:
            query["depth"] = depth
        return await self._get(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/files/list",
            cast_to=SandboxEntryListResponse,
            options=make_request_options(
                query=query, extra_headers=extra_headers, extra_query=extra_query, timeout=timeout
            ),
        )

    async def stat(
        self,
        sandbox_id: str,
        *,
        path: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxEntryResponse:
        validate_identifier(sandbox_id)
        query: dict[str, object] = {}
        if path is not None:
            query["path"] = path
        return await self._get(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/files/stat",
            cast_to=SandboxEntryResponse,
            options=make_request_options(
                query=query, extra_headers=extra_headers, extra_query=extra_query, timeout=timeout
            ),
        )

    async def move(
        self,
        sandbox_id: str,
        *,
        path: str,
        new_path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxFileResponse:
        validate_identifier(sandbox_id)
        validate_required_path(path)
        validate_required_path(new_path)
        return await self._put(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/files/move",
            cast_to=SandboxFileResponse,
            options=make_request_options(
                query={"path": path, "newPath": new_path},
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    async def make_directory(
        self,
        sandbox_id: str,
        *,
        path: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxFileResponse:
        validate_identifier(sandbox_id)
        validate_required_path(path)
        return await self._post(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/dirs",
            cast_to=SandboxFileResponse,
            options=make_request_options(
                query={"path": path},
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )


class FilesResourceWithRawResponse:
    def __init__(self, files: FilesResource) -> None:
        self.upload = to_raw_response_wrapper(files.upload)
        self.download = to_custom_raw_response_wrapper(files.download, BinaryAPIResponse)
        self.delete = to_raw_response_wrapper(files.delete)
        self.list = to_raw_response_wrapper(files.list)
        self.stat = to_raw_response_wrapper(files.stat)
        self.move = to_raw_response_wrapper(files.move)
        self.make_directory = to_raw_response_wrapper(files.make_directory)


class AsyncFilesResourceWithRawResponse:
    def __init__(self, files: AsyncFilesResource) -> None:
        self.upload = async_to_raw_response_wrapper(files.upload)
        self.download = async_to_custom_raw_response_wrapper(files.download, AsyncBinaryAPIResponse)
        self.delete = async_to_raw_response_wrapper(files.delete)
        self.list = async_to_raw_response_wrapper(files.list)
        self.stat = async_to_raw_response_wrapper(files.stat)
        self.move = async_to_raw_response_wrapper(files.move)
        self.make_directory = async_to_raw_response_wrapper(files.make_directory)


class FilesResourceWithStreamingResponse:
    def __init__(self, files: FilesResource) -> None:
        self.upload = to_streamed_response_wrapper(files.upload)
        self.download = to_custom_streamed_response_wrapper(files.download, StreamedBinaryAPIResponse)
        self.delete = to_streamed_response_wrapper(files.delete)
        self.list = to_streamed_response_wrapper(files.list)
        self.stat = to_streamed_response_wrapper(files.stat)
        self.move = to_streamed_response_wrapper(files.move)
        self.make_directory = to_streamed_response_wrapper(files.make_directory)


class AsyncFilesResourceWithStreamingResponse:
    def __init__(self, files: AsyncFilesResource) -> None:
        self.upload = async_to_streamed_response_wrapper(files.upload)
        self.download = async_to_custom_streamed_response_wrapper(files.download, AsyncStreamedBinaryAPIResponse)
        self.delete = async_to_streamed_response_wrapper(files.delete)
        self.list = async_to_streamed_response_wrapper(files.list)
        self.stat = async_to_streamed_response_wrapper(files.stat)
        self.move = async_to_streamed_response_wrapper(files.move)
        self.make_directory = async_to_streamed_response_wrapper(files.make_directory)
