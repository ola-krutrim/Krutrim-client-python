from __future__ import annotations

import httpx

from ._common import PREFIX, prepare, identifier
from ..._types import NOT_GIVEN, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.sandbox_service import (
    TerminalTicketResponse,
)


class TerminalResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TerminalResourceWithRawResponse:
        return TerminalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TerminalResourceWithStreamingResponse:
        return TerminalResourceWithStreamingResponse(self)

    def create_ticket(
        self,
        *,
        krn_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TerminalTicketResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/terminal/ticket. Returns a one-use ticket valid for 60 seconds; connect to details.url."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="terminal.create_ticket",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
            unsafe=True,
        )
        return self._post(
            f"{PREFIX}/sandboxes/{krn_id}/terminal/ticket", cast_to=TerminalTicketResponse, options=options, body=body
        )


class AsyncTerminalResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTerminalResourceWithRawResponse:
        return AsyncTerminalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTerminalResourceWithStreamingResponse:
        return AsyncTerminalResourceWithStreamingResponse(self)

    async def create_ticket(
        self,
        *,
        krn_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TerminalTicketResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/terminal/ticket. Returns a one-use ticket valid for 60 seconds; connect to details.url."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="terminal.create_ticket",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
            unsafe=True,
        )
        return await self._post(
            f"{PREFIX}/sandboxes/{krn_id}/terminal/ticket", cast_to=TerminalTicketResponse, options=options, body=body
        )


class TerminalResourceWithRawResponse:
    def __init__(self, resource: TerminalResource) -> None:
        self.create_ticket = to_raw_response_wrapper(resource.create_ticket)


class TerminalResourceWithStreamingResponse:
    def __init__(self, resource: TerminalResource) -> None:
        self.create_ticket = to_streamed_response_wrapper(resource.create_ticket)


class AsyncTerminalResourceWithRawResponse:
    def __init__(self, resource: AsyncTerminalResource) -> None:
        self.create_ticket = async_to_raw_response_wrapper(resource.create_ticket)


class AsyncTerminalResourceWithStreamingResponse:
    def __init__(self, resource: AsyncTerminalResource) -> None:
        self.create_ticket = async_to_streamed_response_wrapper(resource.create_ticket)
