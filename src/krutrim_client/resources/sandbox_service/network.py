from __future__ import annotations

import httpx

from ._common import PREFIX, prepare, identifier
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.sandbox_service import (
    NetworkResponse,
    NetworkPolicyParams,
)


class NetworkResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NetworkResourceWithRawResponse:
        return NetworkResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NetworkResourceWithStreamingResponse:
        return NetworkResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        krn_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NetworkResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/network."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="network.retrieve",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(f"{PREFIX}/sandboxes/{krn_id}/network", cast_to=NetworkResponse, options=options)

    def update(
        self,
        *,
        krn_id: str,
        x_region: str,
        network: NetworkPolicyParams,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NetworkResponse:
        """PUT /sandbox/v1/sandboxes/{krn_id}/network. Returns immediately; poll the operation before dependent actions."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="network.update",
            x_region=x_region,
            body=dict(network),
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._put(f"{PREFIX}/sandboxes/{krn_id}/network", cast_to=NetworkResponse, options=options, body=body)


class AsyncNetworkResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNetworkResourceWithRawResponse:
        return AsyncNetworkResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNetworkResourceWithStreamingResponse:
        return AsyncNetworkResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        krn_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NetworkResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/network."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="network.retrieve",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(f"{PREFIX}/sandboxes/{krn_id}/network", cast_to=NetworkResponse, options=options)

    async def update(
        self,
        *,
        krn_id: str,
        x_region: str,
        network: NetworkPolicyParams,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NetworkResponse:
        """PUT /sandbox/v1/sandboxes/{krn_id}/network. Returns immediately; poll the operation before dependent actions."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="network.update",
            x_region=x_region,
            body=dict(network),
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._put(
            f"{PREFIX}/sandboxes/{krn_id}/network", cast_to=NetworkResponse, options=options, body=body
        )


class NetworkResourceWithRawResponse:
    def __init__(self, resource: NetworkResource) -> None:
        self.retrieve = to_raw_response_wrapper(resource.retrieve)
        self.update = to_raw_response_wrapper(resource.update)


class NetworkResourceWithStreamingResponse:
    def __init__(self, resource: NetworkResource) -> None:
        self.retrieve = to_streamed_response_wrapper(resource.retrieve)
        self.update = to_streamed_response_wrapper(resource.update)


class AsyncNetworkResourceWithRawResponse:
    def __init__(self, resource: AsyncNetworkResource) -> None:
        self.retrieve = async_to_raw_response_wrapper(resource.retrieve)
        self.update = async_to_raw_response_wrapper(resource.update)


class AsyncNetworkResourceWithStreamingResponse:
    def __init__(self, resource: AsyncNetworkResource) -> None:
        self.retrieve = async_to_streamed_response_wrapper(resource.retrieve)
        self.update = async_to_streamed_response_wrapper(resource.update)
