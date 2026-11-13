from __future__ import annotations

from typing import Dict

import httpx

from ._common import PREFIX, prepare, identifier
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ._streaming import SandboxExecStream, AsyncSandboxExecStream
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.sandbox_service import (
    ExecResponse,
    SandboxStatus,
    UsageResponse,
    SandboxResponse,
    NetworkPolicyParams,
    SandboxListResponse,
)


class SandboxesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SandboxesResourceWithRawResponse:
        return SandboxesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SandboxesResourceWithStreamingResponse:
        return SandboxesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        x_region: str,
        name: str,
        flavor: str,
        template: str | NotGiven = NOT_GIVEN,
        image: str | NotGiven = NOT_GIVEN,
        ttl_seconds: int | NotGiven = NOT_GIVEN,
        env: Dict[str, str] | NotGiven = NOT_GIVEN,
        network: NetworkPolicyParams | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """POST /sandbox/v1/sandboxes. Returns immediately; poll the operation before dependent actions."""
        body, options = prepare(
            self._client,
            action="sandboxes.create",
            x_region=x_region,
            body={
                "name": name,
                "flavor": flavor,
                "template": template,
                "image": image,
                "ttl_seconds": ttl_seconds,
                "env": env,
                "network": network,
            },
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._post(f"{PREFIX}/sandboxes", cast_to=SandboxResponse, options=options, body=body)

    def list(
        self,
        *,
        x_region: str,
        status: SandboxStatus | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxListResponse:
        """GET /sandbox/v1/sandboxes."""
        _body, options = prepare(
            self._client,
            action="sandboxes.list",
            x_region=x_region,
            body={},
            query={"status": status, "name": name, "limit": limit, "offset": offset},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(f"{PREFIX}/sandboxes", cast_to=SandboxListResponse, options=options)

    def retrieve(
        self,
        *,
        krn_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="sandboxes.retrieve",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(f"{PREFIX}/sandboxes/{krn_id}", cast_to=SandboxResponse, options=options)

    def delete(
        self,
        *,
        krn_id: str,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """DELETE /sandbox/v1/sandboxes/{krn_id}. Returns immediately; poll the operation before dependent actions."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.delete",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._delete(f"{PREFIX}/sandboxes/{krn_id}", cast_to=SandboxResponse, options=options, body=body)

    def start(
        self,
        *,
        krn_id: str,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/start. Returns immediately; poll the operation before dependent actions."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.start",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._post(f"{PREFIX}/sandboxes/{krn_id}/start", cast_to=SandboxResponse, options=options, body=body)

    def stop(
        self,
        *,
        krn_id: str,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/stop. Returns immediately; poll the operation before dependent actions."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.stop",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._post(f"{PREFIX}/sandboxes/{krn_id}/stop", cast_to=SandboxResponse, options=options, body=body)

    def extend(
        self,
        *,
        krn_id: str,
        x_region: str,
        ttl_seconds: int,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/extend. Adds ttl_seconds to the current expiry; it does not reset the lifetime."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.extend",
            x_region=x_region,
            body={"ttl_seconds": ttl_seconds},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._post(f"{PREFIX}/sandboxes/{krn_id}/extend", cast_to=SandboxResponse, options=options, body=body)

    def resize(
        self,
        *,
        krn_id: str,
        x_region: str,
        flavor: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/resize. Keeps disk files but discards running processes and memory. Returns immediately; poll the operation before dependent actions."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.resize",
            x_region=x_region,
            body={"flavor": flavor},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._post(f"{PREFIX}/sandboxes/{krn_id}/resize", cast_to=SandboxResponse, options=options, body=body)

    def usage(
        self,
        *,
        krn_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UsageResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/usage."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="sandboxes.usage",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(f"{PREFIX}/sandboxes/{krn_id}/usage", cast_to=UsageResponse, options=options)

    def exec(
        self,
        *,
        krn_id: str,
        x_region: str,
        cmd: str,
        cwd: str | NotGiven = NOT_GIVEN,
        env: Dict[str, str] | NotGiven = NOT_GIVEN,
        stdin: str | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        timeout_seconds: int | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExecResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/exec. Returns HTTP success even for a nonzero command exit_code."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.exec",
            x_region=x_region,
            body={"cmd": cmd, "cwd": cwd, "env": env, "stdin": stdin, "user": user, "timeout_seconds": timeout_seconds},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._post(f"{PREFIX}/sandboxes/{krn_id}/exec", cast_to=ExecResponse, options=options, body=body)

    def exec_stream(
        self,
        *,
        krn_id: str,
        x_region: str,
        cmd: str,
        cwd: str | NotGiven = NOT_GIVEN,
        env: Dict[str, str] | NotGiven = NOT_GIVEN,
        stdin: str | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        timeout_seconds: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxExecStream:
        """POST /sandbox/v1/sandboxes/{krn_id}/exec. Yields named SSE events; close the stream when ending iteration early."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.exec_stream",
            x_region=x_region,
            body={
                "cmd": cmd,
                "cwd": cwd,
                "env": env,
                "stdin": stdin,
                "user": user,
                "timeout_seconds": timeout_seconds,
                "stream": True,
            },
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            unsafe=True,
        )
        return self._post(
            f"{PREFIX}/sandboxes/{krn_id}/exec",
            cast_to=ExecResponse,
            options=options,
            body=body,
            stream=True,
            stream_cls=SandboxExecStream,
        )


class AsyncSandboxesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSandboxesResourceWithRawResponse:
        return AsyncSandboxesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSandboxesResourceWithStreamingResponse:
        return AsyncSandboxesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        x_region: str,
        name: str,
        flavor: str,
        template: str | NotGiven = NOT_GIVEN,
        image: str | NotGiven = NOT_GIVEN,
        ttl_seconds: int | NotGiven = NOT_GIVEN,
        env: Dict[str, str] | NotGiven = NOT_GIVEN,
        network: NetworkPolicyParams | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """POST /sandbox/v1/sandboxes. Returns immediately; poll the operation before dependent actions."""
        body, options = prepare(
            self._client,
            action="sandboxes.create",
            x_region=x_region,
            body={
                "name": name,
                "flavor": flavor,
                "template": template,
                "image": image,
                "ttl_seconds": ttl_seconds,
                "env": env,
                "network": network,
            },
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._post(f"{PREFIX}/sandboxes", cast_to=SandboxResponse, options=options, body=body)

    async def list(
        self,
        *,
        x_region: str,
        status: SandboxStatus | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxListResponse:
        """GET /sandbox/v1/sandboxes."""
        _body, options = prepare(
            self._client,
            action="sandboxes.list",
            x_region=x_region,
            body={},
            query={"status": status, "name": name, "limit": limit, "offset": offset},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(f"{PREFIX}/sandboxes", cast_to=SandboxListResponse, options=options)

    async def retrieve(
        self,
        *,
        krn_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="sandboxes.retrieve",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(f"{PREFIX}/sandboxes/{krn_id}", cast_to=SandboxResponse, options=options)

    async def delete(
        self,
        *,
        krn_id: str,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """DELETE /sandbox/v1/sandboxes/{krn_id}. Returns immediately; poll the operation before dependent actions."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.delete",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._delete(f"{PREFIX}/sandboxes/{krn_id}", cast_to=SandboxResponse, options=options, body=body)

    async def start(
        self,
        *,
        krn_id: str,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/start. Returns immediately; poll the operation before dependent actions."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.start",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._post(
            f"{PREFIX}/sandboxes/{krn_id}/start", cast_to=SandboxResponse, options=options, body=body
        )

    async def stop(
        self,
        *,
        krn_id: str,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/stop. Returns immediately; poll the operation before dependent actions."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.stop",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._post(
            f"{PREFIX}/sandboxes/{krn_id}/stop", cast_to=SandboxResponse, options=options, body=body
        )

    async def extend(
        self,
        *,
        krn_id: str,
        x_region: str,
        ttl_seconds: int,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/extend. Adds ttl_seconds to the current expiry; it does not reset the lifetime."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.extend",
            x_region=x_region,
            body={"ttl_seconds": ttl_seconds},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._post(
            f"{PREFIX}/sandboxes/{krn_id}/extend", cast_to=SandboxResponse, options=options, body=body
        )

    async def resize(
        self,
        *,
        krn_id: str,
        x_region: str,
        flavor: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/resize. Keeps disk files but discards running processes and memory. Returns immediately; poll the operation before dependent actions."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.resize",
            x_region=x_region,
            body={"flavor": flavor},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._post(
            f"{PREFIX}/sandboxes/{krn_id}/resize", cast_to=SandboxResponse, options=options, body=body
        )

    async def usage(
        self,
        *,
        krn_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UsageResponse:
        """GET /sandbox/v1/sandboxes/{krn_id}/usage."""
        krn_id = identifier(krn_id, "krn_id")
        _body, options = prepare(
            self._client,
            action="sandboxes.usage",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(f"{PREFIX}/sandboxes/{krn_id}/usage", cast_to=UsageResponse, options=options)

    async def exec(
        self,
        *,
        krn_id: str,
        x_region: str,
        cmd: str,
        cwd: str | NotGiven = NOT_GIVEN,
        env: Dict[str, str] | NotGiven = NOT_GIVEN,
        stdin: str | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        timeout_seconds: int | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ExecResponse:
        """POST /sandbox/v1/sandboxes/{krn_id}/exec. Returns HTTP success even for a nonzero command exit_code."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.exec",
            x_region=x_region,
            body={"cmd": cmd, "cwd": cwd, "env": env, "stdin": stdin, "user": user, "timeout_seconds": timeout_seconds},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._post(f"{PREFIX}/sandboxes/{krn_id}/exec", cast_to=ExecResponse, options=options, body=body)

    async def exec_stream(
        self,
        *,
        krn_id: str,
        x_region: str,
        cmd: str,
        cwd: str | NotGiven = NOT_GIVEN,
        env: Dict[str, str] | NotGiven = NOT_GIVEN,
        stdin: str | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        timeout_seconds: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSandboxExecStream:
        """POST /sandbox/v1/sandboxes/{krn_id}/exec. Yields named SSE events; close the stream when ending iteration early."""
        krn_id = identifier(krn_id, "krn_id")
        body, options = prepare(
            self._client,
            action="sandboxes.exec_stream",
            x_region=x_region,
            body={
                "cmd": cmd,
                "cwd": cwd,
                "env": env,
                "stdin": stdin,
                "user": user,
                "timeout_seconds": timeout_seconds,
                "stream": True,
            },
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            unsafe=True,
        )
        return await self._post(
            f"{PREFIX}/sandboxes/{krn_id}/exec",
            cast_to=ExecResponse,
            options=options,
            body=body,
            stream=True,
            stream_cls=AsyncSandboxExecStream,
        )


class SandboxesResourceWithRawResponse:
    def __init__(self, resource: SandboxesResource) -> None:
        self.create = to_raw_response_wrapper(resource.create)
        self.list = to_raw_response_wrapper(resource.list)
        self.retrieve = to_raw_response_wrapper(resource.retrieve)
        self.delete = to_raw_response_wrapper(resource.delete)
        self.start = to_raw_response_wrapper(resource.start)
        self.stop = to_raw_response_wrapper(resource.stop)
        self.extend = to_raw_response_wrapper(resource.extend)
        self.resize = to_raw_response_wrapper(resource.resize)
        self.usage = to_raw_response_wrapper(resource.usage)
        self.exec = to_raw_response_wrapper(resource.exec)
        self.exec_stream = to_raw_response_wrapper(resource.exec_stream)


class SandboxesResourceWithStreamingResponse:
    def __init__(self, resource: SandboxesResource) -> None:
        self.create = to_streamed_response_wrapper(resource.create)
        self.list = to_streamed_response_wrapper(resource.list)
        self.retrieve = to_streamed_response_wrapper(resource.retrieve)
        self.delete = to_streamed_response_wrapper(resource.delete)
        self.start = to_streamed_response_wrapper(resource.start)
        self.stop = to_streamed_response_wrapper(resource.stop)
        self.extend = to_streamed_response_wrapper(resource.extend)
        self.resize = to_streamed_response_wrapper(resource.resize)
        self.usage = to_streamed_response_wrapper(resource.usage)
        self.exec = to_streamed_response_wrapper(resource.exec)
        self.exec_stream = to_streamed_response_wrapper(resource.exec_stream)


class AsyncSandboxesResourceWithRawResponse:
    def __init__(self, resource: AsyncSandboxesResource) -> None:
        self.create = async_to_raw_response_wrapper(resource.create)
        self.list = async_to_raw_response_wrapper(resource.list)
        self.retrieve = async_to_raw_response_wrapper(resource.retrieve)
        self.delete = async_to_raw_response_wrapper(resource.delete)
        self.start = async_to_raw_response_wrapper(resource.start)
        self.stop = async_to_raw_response_wrapper(resource.stop)
        self.extend = async_to_raw_response_wrapper(resource.extend)
        self.resize = async_to_raw_response_wrapper(resource.resize)
        self.usage = async_to_raw_response_wrapper(resource.usage)
        self.exec = async_to_raw_response_wrapper(resource.exec)
        self.exec_stream = async_to_raw_response_wrapper(resource.exec_stream)


class AsyncSandboxesResourceWithStreamingResponse:
    def __init__(self, resource: AsyncSandboxesResource) -> None:
        self.create = async_to_streamed_response_wrapper(resource.create)
        self.list = async_to_streamed_response_wrapper(resource.list)
        self.retrieve = async_to_streamed_response_wrapper(resource.retrieve)
        self.delete = async_to_streamed_response_wrapper(resource.delete)
        self.start = async_to_streamed_response_wrapper(resource.start)
        self.stop = async_to_streamed_response_wrapper(resource.stop)
        self.extend = async_to_streamed_response_wrapper(resource.extend)
        self.resize = async_to_streamed_response_wrapper(resource.resize)
        self.usage = async_to_streamed_response_wrapper(resource.usage)
        self.exec = async_to_streamed_response_wrapper(resource.exec)
        self.exec_stream = async_to_streamed_response_wrapper(resource.exec_stream)
