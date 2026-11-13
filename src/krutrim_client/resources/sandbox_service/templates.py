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
    TemplateResponse,
    TemplateListResponse,
    TemplateDeleteResponse,
)


class TemplatesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TemplatesResourceWithRawResponse:
        return TemplatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TemplatesResourceWithStreamingResponse:
        return TemplatesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        x_region: str,
        name: str,
        image: str,
        description: str | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TemplateResponse:
        """POST /sandbox/v1/templates."""
        body, options = prepare(
            self._client,
            action="templates.create",
            x_region=x_region,
            body={"name": name, "image": image, "description": description},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return self._post(f"{PREFIX}/templates", cast_to=TemplateResponse, options=options, body=body)

    def list(
        self,
        *,
        x_region: str,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TemplateListResponse:
        """GET /sandbox/v1/templates."""
        _body, options = prepare(
            self._client,
            action="templates.list",
            x_region=x_region,
            body={},
            query={"limit": limit, "offset": offset},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(f"{PREFIX}/templates", cast_to=TemplateListResponse, options=options)

    def retrieve(
        self,
        *,
        template_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TemplateResponse:
        """GET /sandbox/v1/templates/{template_id}."""
        template_id = identifier(template_id, "template_id")
        _body, options = prepare(
            self._client,
            action="templates.retrieve",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return self._get(f"{PREFIX}/templates/{template_id}", cast_to=TemplateResponse, options=options)

    def delete(
        self,
        *,
        template_id: str,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TemplateDeleteResponse:
        """DELETE /sandbox/v1/templates/{template_id}."""
        template_id = identifier(template_id, "template_id")
        body, options = prepare(
            self._client,
            action="templates.delete",
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
        return self._delete(
            f"{PREFIX}/templates/{template_id}", cast_to=TemplateDeleteResponse, options=options, body=body
        )


class AsyncTemplatesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTemplatesResourceWithRawResponse:
        return AsyncTemplatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTemplatesResourceWithStreamingResponse:
        return AsyncTemplatesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        x_region: str,
        name: str,
        image: str,
        description: str | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TemplateResponse:
        """POST /sandbox/v1/templates."""
        body, options = prepare(
            self._client,
            action="templates.create",
            x_region=x_region,
            body={"name": name, "image": image, "description": description},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            mutation=True,
            idempotency_key=idempotency_key,
        )
        return await self._post(f"{PREFIX}/templates", cast_to=TemplateResponse, options=options, body=body)

    async def list(
        self,
        *,
        x_region: str,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TemplateListResponse:
        """GET /sandbox/v1/templates."""
        _body, options = prepare(
            self._client,
            action="templates.list",
            x_region=x_region,
            body={},
            query={"limit": limit, "offset": offset},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(f"{PREFIX}/templates", cast_to=TemplateListResponse, options=options)

    async def retrieve(
        self,
        *,
        template_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TemplateResponse:
        """GET /sandbox/v1/templates/{template_id}."""
        template_id = identifier(template_id, "template_id")
        _body, options = prepare(
            self._client,
            action="templates.retrieve",
            x_region=x_region,
            body={},
            query={},
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=None,
            timeout=timeout,
        )
        return await self._get(f"{PREFIX}/templates/{template_id}", cast_to=TemplateResponse, options=options)

    async def delete(
        self,
        *,
        template_id: str,
        x_region: str,
        idempotency_key: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TemplateDeleteResponse:
        """DELETE /sandbox/v1/templates/{template_id}."""
        template_id = identifier(template_id, "template_id")
        body, options = prepare(
            self._client,
            action="templates.delete",
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
        return await self._delete(
            f"{PREFIX}/templates/{template_id}", cast_to=TemplateDeleteResponse, options=options, body=body
        )


class TemplatesResourceWithRawResponse:
    def __init__(self, resource: TemplatesResource) -> None:
        self.create = to_raw_response_wrapper(resource.create)
        self.list = to_raw_response_wrapper(resource.list)
        self.retrieve = to_raw_response_wrapper(resource.retrieve)
        self.delete = to_raw_response_wrapper(resource.delete)


class TemplatesResourceWithStreamingResponse:
    def __init__(self, resource: TemplatesResource) -> None:
        self.create = to_streamed_response_wrapper(resource.create)
        self.list = to_streamed_response_wrapper(resource.list)
        self.retrieve = to_streamed_response_wrapper(resource.retrieve)
        self.delete = to_streamed_response_wrapper(resource.delete)


class AsyncTemplatesResourceWithRawResponse:
    def __init__(self, resource: AsyncTemplatesResource) -> None:
        self.create = async_to_raw_response_wrapper(resource.create)
        self.list = async_to_raw_response_wrapper(resource.list)
        self.retrieve = async_to_raw_response_wrapper(resource.retrieve)
        self.delete = async_to_raw_response_wrapper(resource.delete)


class AsyncTemplatesResourceWithStreamingResponse:
    def __init__(self, resource: AsyncTemplatesResource) -> None:
        self.create = async_to_streamed_response_wrapper(resource.create)
        self.list = async_to_streamed_response_wrapper(resource.list)
        self.retrieve = async_to_streamed_response_wrapper(resource.retrieve)
        self.delete = async_to_streamed_response_wrapper(resource.delete)
