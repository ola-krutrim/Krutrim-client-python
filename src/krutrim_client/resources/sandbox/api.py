from __future__ import annotations

from typing import Any, List, Mapping, Sequence, cast

import httpx

from .files import (
    FilesResource,
    AsyncFilesResource,
    FilesResourceWithRawResponse,
    AsyncFilesResourceWithRawResponse,
    FilesResourceWithStreamingResponse,
    AsyncFilesResourceWithStreamingResponse,
)
from .ports import (
    PortsResource,
    AsyncPortsResource,
    PortsResourceWithRawResponse,
    AsyncPortsResourceWithRawResponse,
    PortsResourceWithStreamingResponse,
    AsyncPortsResourceWithStreamingResponse,
)
from .proxy import (
    ProxyResource,
    AsyncProxyResource,
    ProxyResourceWithRawResponse,
    AsyncProxyResourceWithRawResponse,
    ProxyResourceWithStreamingResponse,
    AsyncProxyResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ._helpers import validate_ttl, validate_identifier, validate_sandbox_name
from .commands import (
    CommandsResource,
    AsyncCommandsResource,
    CommandsResourceWithRawResponse,
    AsyncCommandsResourceWithRawResponse,
    CommandsResourceWithStreamingResponse,
    AsyncCommandsResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.sandbox import (
    PodTemplate,
    SandboxListParams,
    FlavorListResponse,
    SandboxGetResponse,
    SandboxTTLResponse,
    SandboxCreateParams,
    SandboxListResponse,
    SandboxSetTTLParams,
    AsyncSandboxResponse,
    SandboxDeleteResponse,
    NetworkStorageAttachmentInput,
)

__all__ = ["SandboxAPIResource", "AsyncSandboxAPIResource"]


def _validate_create(
    *,
    sandbox_name: str,
    template_id: int | None,
    template_name: str | None,
    network_storages: Sequence[NetworkStorageAttachmentInput] | None,
    ttl_seconds: int | None,
) -> None:
    validate_sandbox_name(sandbox_name)
    if template_id is not None and template_name is not None:
        raise ValueError("template_id and template_name are mutually exclusive")
    if network_storages is not None and len(network_storages) > 10:
        raise ValueError("at most 10 network storage attachments are supported")
    if ttl_seconds is not None:
        validate_ttl(ttl_seconds)


class SandboxAPIResource(SyncAPIResource):
    @cached_property
    def files(self) -> FilesResource:
        return FilesResource(self._client)

    @cached_property
    def commands(self) -> CommandsResource:
        return CommandsResource(self._client)

    @cached_property
    def ports(self) -> PortsResource:
        return PortsResource(self._client)

    @cached_property
    def proxy(self) -> ProxyResource:
        return ProxyResource(self._client)

    @cached_property
    def with_raw_response(self) -> SandboxAPIResourceWithRawResponse:
        return SandboxAPIResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SandboxAPIResourceWithStreamingResponse:
        return SandboxAPIResourceWithStreamingResponse(self)

    def list_templates(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> List[PodTemplate]:
        return cast(
            List[PodTemplate],
            self._get(
                "/omni/sandbox/v1/template",
                cast_to=cast(Any, List[PodTemplate]),
                options=make_request_options(extra_headers=extra_headers, extra_query=extra_query, timeout=timeout),
            ),
        )

    def list_flavors(
        self,
        *,
        region: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FlavorListResponse:
        query: dict[str, object] = {}
        if region is not None:
            query["region"] = region
        return self._get(
            "/omni/sandbox/v1/flavors",
            cast_to=FlavorListResponse,
            options=make_request_options(
                query=query, extra_headers=extra_headers, extra_query=extra_query, timeout=timeout
            ),
        )

    def list(
        self,
        *,
        region: str | None = None,
        status: str | None = None,
        name: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxListResponse:
        if page is not None and page < 1:
            raise ValueError("page must be at least 1")
        if limit is not None and not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        query = {
            key: value
            for key, value in locals().items()
            if key in {"region", "status", "name", "page", "limit"} and value is not None
        }
        return self._get(
            "/omni/sandbox/v1/sandbox",
            cast_to=SandboxListResponse,
            options=make_request_options(
                query=maybe_transform(query, SandboxListParams),
                extra_headers=extra_headers,
                extra_query=extra_query,
                timeout=timeout,
            ),
        )

    def create(
        self,
        *,
        sandbox_name: str,
        region: str,
        flavor_name: str,
        template_id: int | None = None,
        template_name: str | None = None,
        network_storages: Sequence[NetworkStorageAttachmentInput] | None = None,
        environment_variables: Mapping[str, str] | None = None,
        ttl_seconds: int | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSandboxResponse:
        _validate_create(
            sandbox_name=sandbox_name,
            template_id=template_id,
            template_name=template_name,
            network_storages=network_storages,
            ttl_seconds=ttl_seconds,
        )
        body: dict[str, object] = {
            "sandbox_name": sandbox_name,
            "region": region,
            "flavor_name": flavor_name,
        }
        if network_storages is not None:
            body["network_storages"] = list(network_storages)
        for key, value in {
            "template_id": template_id,
            "template_name": template_name,
            "environment_variables": environment_variables,
            "ttl_seconds": ttl_seconds,
        }.items():
            if value is not None:
                body[key] = value
        return self._post(
            "/omni/sandbox/v1/sandbox",
            cast_to=AsyncSandboxResponse,
            body=maybe_transform(body, SandboxCreateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    def retrieve(
        self,
        sandbox_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxGetResponse:
        validate_identifier(sandbox_id)
        return self._get(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}",
            cast_to=SandboxGetResponse,
            options=make_request_options(extra_headers=extra_headers, extra_query=extra_query, timeout=timeout),
        )

    def set_ttl(
        self,
        sandbox_id: str,
        ttl_seconds: int,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxTTLResponse:
        validate_identifier(sandbox_id)
        validate_ttl(ttl_seconds)
        return self._post(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/ttl",
            cast_to=SandboxTTLResponse,
            body=maybe_transform({"ttl_seconds": ttl_seconds}, SandboxSetTTLParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    def delete(
        self,
        sandbox_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxDeleteResponse:
        validate_identifier(sandbox_id)
        return self._delete(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}",
            cast_to=SandboxDeleteResponse,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )


class AsyncSandboxAPIResource(AsyncAPIResource):
    @cached_property
    def files(self) -> AsyncFilesResource:
        return AsyncFilesResource(self._client)

    @cached_property
    def commands(self) -> AsyncCommandsResource:
        return AsyncCommandsResource(self._client)

    @cached_property
    def ports(self) -> AsyncPortsResource:
        return AsyncPortsResource(self._client)

    @cached_property
    def proxy(self) -> AsyncProxyResource:
        return AsyncProxyResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSandboxAPIResourceWithRawResponse:
        return AsyncSandboxAPIResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSandboxAPIResourceWithStreamingResponse:
        return AsyncSandboxAPIResourceWithStreamingResponse(self)

    async def list_templates(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> List[PodTemplate]:
        return cast(
            List[PodTemplate],
            await self._get(
                "/omni/sandbox/v1/template",
                cast_to=cast(Any, List[PodTemplate]),
                options=make_request_options(extra_headers=extra_headers, extra_query=extra_query, timeout=timeout),
            ),
        )

    async def list_flavors(
        self,
        *,
        region: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FlavorListResponse:
        query: dict[str, object] = {}
        if region is not None:
            query["region"] = region
        return await self._get(
            "/omni/sandbox/v1/flavors",
            cast_to=FlavorListResponse,
            options=make_request_options(
                query=query, extra_headers=extra_headers, extra_query=extra_query, timeout=timeout
            ),
        )

    async def list(
        self,
        *,
        region: str | None = None,
        status: str | None = None,
        name: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxListResponse:
        if page is not None and page < 1:
            raise ValueError("page must be at least 1")
        if limit is not None and not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        query = {
            key: value
            for key, value in locals().items()
            if key in {"region", "status", "name", "page", "limit"} and value is not None
        }
        return await self._get(
            "/omni/sandbox/v1/sandbox",
            cast_to=SandboxListResponse,
            options=make_request_options(
                query=await async_maybe_transform(query, SandboxListParams),
                extra_headers=extra_headers,
                extra_query=extra_query,
                timeout=timeout,
            ),
        )

    async def create(
        self,
        *,
        sandbox_name: str,
        region: str,
        flavor_name: str,
        template_id: int | None = None,
        template_name: str | None = None,
        network_storages: Sequence[NetworkStorageAttachmentInput] | None = None,
        environment_variables: Mapping[str, str] | None = None,
        ttl_seconds: int | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSandboxResponse:
        _validate_create(
            sandbox_name=sandbox_name,
            template_id=template_id,
            template_name=template_name,
            network_storages=network_storages,
            ttl_seconds=ttl_seconds,
        )
        body: dict[str, object] = {
            "sandbox_name": sandbox_name,
            "region": region,
            "flavor_name": flavor_name,
        }
        if network_storages is not None:
            body["network_storages"] = list(network_storages)
        for key, value in {
            "template_id": template_id,
            "template_name": template_name,
            "environment_variables": environment_variables,
            "ttl_seconds": ttl_seconds,
        }.items():
            if value is not None:
                body[key] = value
        return await self._post(
            "/omni/sandbox/v1/sandbox",
            cast_to=AsyncSandboxResponse,
            body=await async_maybe_transform(body, SandboxCreateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    async def retrieve(
        self,
        sandbox_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxGetResponse:
        validate_identifier(sandbox_id)
        return await self._get(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}",
            cast_to=SandboxGetResponse,
            options=make_request_options(extra_headers=extra_headers, extra_query=extra_query, timeout=timeout),
        )

    async def set_ttl(
        self,
        sandbox_id: str,
        ttl_seconds: int,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxTTLResponse:
        validate_identifier(sandbox_id)
        validate_ttl(ttl_seconds)
        return await self._post(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}/ttl",
            cast_to=SandboxTTLResponse,
            body=await async_maybe_transform({"ttl_seconds": ttl_seconds}, SandboxSetTTLParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    async def delete(
        self,
        sandbox_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SandboxDeleteResponse:
        validate_identifier(sandbox_id)
        return await self._delete(
            f"/omni/sandbox/v1/sandbox/{sandbox_id}",
            cast_to=SandboxDeleteResponse,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )


class SandboxAPIResourceWithRawResponse:
    def __init__(self, api: SandboxAPIResource) -> None:
        self._api = api
        self.list_templates = to_raw_response_wrapper(api.list_templates)
        self.list_flavors = to_raw_response_wrapper(api.list_flavors)
        self.list = to_raw_response_wrapper(api.list)
        self.create = to_raw_response_wrapper(api.create)
        self.retrieve = to_raw_response_wrapper(api.retrieve)
        self.set_ttl = to_raw_response_wrapper(api.set_ttl)
        self.delete = to_raw_response_wrapper(api.delete)

    @cached_property
    def files(self) -> FilesResourceWithRawResponse:
        return FilesResourceWithRawResponse(self._api.files)

    @cached_property
    def commands(self) -> CommandsResourceWithRawResponse:
        return CommandsResourceWithRawResponse(self._api.commands)

    @cached_property
    def ports(self) -> PortsResourceWithRawResponse:
        return PortsResourceWithRawResponse(self._api.ports)

    @cached_property
    def proxy(self) -> ProxyResourceWithRawResponse:
        return ProxyResourceWithRawResponse(self._api.proxy)


class AsyncSandboxAPIResourceWithRawResponse:
    def __init__(self, api: AsyncSandboxAPIResource) -> None:
        self._api = api
        self.list_templates = async_to_raw_response_wrapper(api.list_templates)
        self.list_flavors = async_to_raw_response_wrapper(api.list_flavors)
        self.list = async_to_raw_response_wrapper(api.list)
        self.create = async_to_raw_response_wrapper(api.create)
        self.retrieve = async_to_raw_response_wrapper(api.retrieve)
        self.set_ttl = async_to_raw_response_wrapper(api.set_ttl)
        self.delete = async_to_raw_response_wrapper(api.delete)

    @cached_property
    def files(self) -> AsyncFilesResourceWithRawResponse:
        return AsyncFilesResourceWithRawResponse(self._api.files)

    @cached_property
    def commands(self) -> AsyncCommandsResourceWithRawResponse:
        return AsyncCommandsResourceWithRawResponse(self._api.commands)

    @cached_property
    def ports(self) -> AsyncPortsResourceWithRawResponse:
        return AsyncPortsResourceWithRawResponse(self._api.ports)

    @cached_property
    def proxy(self) -> AsyncProxyResourceWithRawResponse:
        return AsyncProxyResourceWithRawResponse(self._api.proxy)


class SandboxAPIResourceWithStreamingResponse:
    def __init__(self, api: SandboxAPIResource) -> None:
        self._api = api
        self.list_templates = to_streamed_response_wrapper(api.list_templates)
        self.list_flavors = to_streamed_response_wrapper(api.list_flavors)
        self.list = to_streamed_response_wrapper(api.list)
        self.create = to_streamed_response_wrapper(api.create)
        self.retrieve = to_streamed_response_wrapper(api.retrieve)
        self.set_ttl = to_streamed_response_wrapper(api.set_ttl)
        self.delete = to_streamed_response_wrapper(api.delete)

    @cached_property
    def files(self) -> FilesResourceWithStreamingResponse:
        return FilesResourceWithStreamingResponse(self._api.files)

    @cached_property
    def commands(self) -> CommandsResourceWithStreamingResponse:
        return CommandsResourceWithStreamingResponse(self._api.commands)

    @cached_property
    def ports(self) -> PortsResourceWithStreamingResponse:
        return PortsResourceWithStreamingResponse(self._api.ports)

    @cached_property
    def proxy(self) -> ProxyResourceWithStreamingResponse:
        return ProxyResourceWithStreamingResponse(self._api.proxy)


class AsyncSandboxAPIResourceWithStreamingResponse:
    def __init__(self, api: AsyncSandboxAPIResource) -> None:
        self._api = api
        self.list_templates = async_to_streamed_response_wrapper(api.list_templates)
        self.list_flavors = async_to_streamed_response_wrapper(api.list_flavors)
        self.list = async_to_streamed_response_wrapper(api.list)
        self.create = async_to_streamed_response_wrapper(api.create)
        self.retrieve = async_to_streamed_response_wrapper(api.retrieve)
        self.set_ttl = async_to_streamed_response_wrapper(api.set_ttl)
        self.delete = async_to_streamed_response_wrapper(api.delete)

    @cached_property
    def files(self) -> AsyncFilesResourceWithStreamingResponse:
        return AsyncFilesResourceWithStreamingResponse(self._api.files)

    @cached_property
    def commands(self) -> AsyncCommandsResourceWithStreamingResponse:
        return AsyncCommandsResourceWithStreamingResponse(self._api.commands)

    @cached_property
    def ports(self) -> AsyncPortsResourceWithStreamingResponse:
        return AsyncPortsResourceWithStreamingResponse(self._api.ports)

    @cached_property
    def proxy(self) -> AsyncProxyResourceWithStreamingResponse:
        return AsyncProxyResourceWithStreamingResponse(self._api.proxy)
