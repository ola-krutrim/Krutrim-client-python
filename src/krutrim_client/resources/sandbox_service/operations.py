from __future__ import annotations

import json
import time
import queue
import threading
import contextvars
from typing import Callable

import anyio
import httpx

from ._common import PREFIX, prepare, identifier, positive_seconds
from ..._types import NOT_GIVEN, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    APIResponse,
    ResponseContextManager,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ._exceptions import SandboxOperationError, SandboxOperationTimeoutError
from ...types.sandbox_service import (
    OperationResponse,
)


class _PollDeadlineExceeded(Exception):
    pass


def _poll_before_deadline(
    resource: OperationsResource,
    deadline: float,
    retrieve: Callable[[], ResponseContextManager[APIResponse[OperationResponse]]],
) -> OperationResponse:
    # HTTPX bounds individual reads, not the entire response. Keep the caller's
    # deadline independent of a peer that sends an indefinitely progressing body.
    results: queue.Queue[OperationResponse | BaseException] = queue.Queue(maxsize=1)
    cancelled = threading.Event()

    def poll() -> None:
        try:
            if cancelled.is_set() or time.monotonic() >= deadline:
                raise _PollDeadlineExceeded()
            with retrieve() as response:
                chunks: list[bytes] = []
                for chunk in response.iter_bytes():
                    if cancelled.is_set() or time.monotonic() >= deadline:
                        raise _PollDeadlineExceeded()
                    chunks.append(chunk)
                result = resource._client._process_response_data(
                    data=json.loads(b"".join(chunks)), cast_to=OperationResponse, response=response.http_response
                )
            results.put(result)
        except BaseException as exc:
            results.put(exc)

    context = contextvars.copy_context()
    # The worker owns and closes its response, including after a timeout. A
    # daemon avoids trapping shutdown on an uncooperative custom transport.
    threading.Thread(target=context.run, args=(poll,), daemon=True, name="krutrim-operation-poll").start()
    try:
        result = results.get(timeout=max(0, deadline - time.monotonic()))
    except queue.Empty as exc:
        cancelled.set()
        raise _PollDeadlineExceeded() from exc
    except BaseException:
        cancelled.set()
        raise
    if isinstance(result, BaseException):
        raise result
    return result


class OperationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OperationsResourceWithRawResponse:
        return OperationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OperationsResourceWithStreamingResponse:
        return OperationsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        operation_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OperationResponse:
        """GET /sandbox/v1/operations/{operation_id}."""
        operation_id = identifier(operation_id, "operation_id")
        _body, options = prepare(
            self._client,
            action="operations.retrieve",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(f"{PREFIX}/operations/{operation_id}", cast_to=OperationResponse, options=options)

    def wait(
        self,
        operation_id: str,
        *,
        x_region: str,
        timeout_seconds: float = 600,
        poll_interval_seconds: float = 2,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OperationResponse:
        """Poll with a bounded deadline; timing out never cancels the server operation."""
        identifier(operation_id, "operation_id")
        positive_seconds(timeout_seconds, "timeout_seconds")
        positive_seconds(poll_interval_seconds, "poll_interval_seconds")
        deadline = time.monotonic() + timeout_seconds
        operation: OperationResponse | None = None
        # Disable inner retries/backoff so the waiter owns its deadline.
        resource = self._client.with_options(max_retries=0).sandbox.operations
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise SandboxOperationTimeoutError(operation_id, operation)
            configured = self._client.timeout if isinstance(timeout, NotGiven) else timeout
            request_timeout = httpx.Timeout(configured)
            request_timeout = httpx.Timeout(
                **{
                    phase: min(value, remaining) if value is not None else remaining
                    for phase, value in request_timeout.as_dict().items()
                }
            )
            try:
                operation = _poll_before_deadline(
                    resource,
                    deadline,
                    lambda request_timeout=request_timeout: resource.with_streaming_response.retrieve(
                        operation_id=operation_id,
                        x_region=x_region,
                        extra_headers=extra_headers,
                        extra_query=extra_query,
                        timeout=request_timeout,
                    ),
                )
            except _PollDeadlineExceeded as exc:
                raise SandboxOperationTimeoutError(operation_id, operation) from exc
            if time.monotonic() >= deadline:
                raise SandboxOperationTimeoutError(operation_id, operation)
            if operation.details.state == "succeeded":
                return operation
            if operation.details.state == "failed":
                raise SandboxOperationError(operation)
            self._sleep(min(poll_interval_seconds, max(0, deadline - time.monotonic())))


class AsyncOperationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOperationsResourceWithRawResponse:
        return AsyncOperationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOperationsResourceWithStreamingResponse:
        return AsyncOperationsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        operation_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OperationResponse:
        """GET /sandbox/v1/operations/{operation_id}."""
        operation_id = identifier(operation_id, "operation_id")
        _body, options = prepare(
            self._client,
            action="operations.retrieve",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(f"{PREFIX}/operations/{operation_id}", cast_to=OperationResponse, options=options)

    async def wait(
        self,
        operation_id: str,
        *,
        x_region: str,
        timeout_seconds: float = 600,
        poll_interval_seconds: float = 2,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OperationResponse:
        """Poll with a bounded deadline; timing out never cancels the server operation."""
        identifier(operation_id, "operation_id")
        positive_seconds(timeout_seconds, "timeout_seconds")
        positive_seconds(poll_interval_seconds, "poll_interval_seconds")
        deadline = time.monotonic() + timeout_seconds
        operation: OperationResponse | None = None
        # Disable inner retries/backoff so the waiter owns its deadline.
        resource = self._client.with_options(max_retries=0).sandbox.operations
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise SandboxOperationTimeoutError(operation_id, operation)
            configured = self._client.timeout if isinstance(timeout, NotGiven) else timeout
            request_timeout = httpx.Timeout(configured)
            request_timeout = httpx.Timeout(
                **{
                    phase: min(value, remaining) if value is not None else remaining
                    for phase, value in request_timeout.as_dict().items()
                }
            )
            try:
                with anyio.fail_after(remaining):
                    operation = await resource.retrieve(
                        operation_id=operation_id,
                        x_region=x_region,
                        extra_headers=extra_headers,
                        extra_query=extra_query,
                        timeout=request_timeout,
                    )
            except TimeoutError as exc:
                raise SandboxOperationTimeoutError(operation_id, operation) from exc
            if time.monotonic() >= deadline:
                raise SandboxOperationTimeoutError(operation_id, operation)
            if operation.details.state == "succeeded":
                return operation
            if operation.details.state == "failed":
                raise SandboxOperationError(operation)
            await self._sleep(min(poll_interval_seconds, max(0, deadline - time.monotonic())))


class OperationsResourceWithRawResponse:
    def __init__(self, resource: OperationsResource) -> None:
        self.retrieve = to_raw_response_wrapper(resource.retrieve)


class OperationsResourceWithStreamingResponse:
    def __init__(self, resource: OperationsResource) -> None:
        self.retrieve = to_streamed_response_wrapper(resource.retrieve)


class AsyncOperationsResourceWithRawResponse:
    def __init__(self, resource: AsyncOperationsResource) -> None:
        self.retrieve = async_to_raw_response_wrapper(resource.retrieve)


class AsyncOperationsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncOperationsResource) -> None:
        self.retrieve = async_to_streamed_response_wrapper(resource.retrieve)
