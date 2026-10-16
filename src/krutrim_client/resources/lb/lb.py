from __future__ import annotations

from typing import Iterable
from urllib.parse import quote

import httpx

from ..._types import NOT_GIVEN, Body, Omit, Query, Headers, NoneType, NotGiven, omit
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._regions import SUPPORTED_REGIONS, unsupported_region_error
from ..._exceptions import APIStatusError
from ...types.lb import (
    create_target_group_params,
    update_target_group_params,
    create_load_balancer_params,
    update_load_balancer_params,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.lb.list_target_groups_response import ListTargetGroupsResponse
from ...types.lb.create_target_group_response import CreateTargetGroupResponse
from ...types.lb.delete_target_group_response import DeleteTargetGroupResponse
from ...types.lb.list_load_balancers_response import ListLoadBalancersResponse
from ...types.lb.update_target_group_response import UpdateTargetGroupResponse
from ...types.lb.create_load_balancer_response import CreateLoadBalancerResponse

__all__ = [
    "LoadBalancerResource",
    "AsyncLoadBalancerResource",
    "LoadBalancerResourceWithRawResponse",
    "AsyncLoadBalancerResourceWithRawResponse",
    "LoadBalancerResourceWithStreamingResponse",
    "AsyncLoadBalancerResourceWithStreamingResponse",
    "LoadBalancerErrorResponse",
    "HighlvlResource",
    "AsyncHighlvlResource",
    "HighlvlResourceWithRawResponse",
    "AsyncHighlvlResourceWithRawResponse",
    "HighlvlResourceWithStreamingResponse",
    "AsyncHighlvlResourceWithStreamingResponse",
]



class LoadBalancerErrorResponse(dict):
    """The (already-parsed) error body returned by the Load Balancer API.

    Instead of raising ``APIStatusError`` (and surfacing a Python traceback),
    every ``client.lb`` method - including the ``.with_raw_response`` and
    ``.with_streaming_response`` variants - returns an instance of this class
    when the API responds with a 4xx/5xx status code. It behaves like the
    parsed JSON error body (a ``dict``) while also exposing ``status_code``,
    ``json()`` and a no-op ``close()``/``aclose()`` so it can be used as a
    drop-in replacement wherever a normal/raw/streamed response is expected.
    """

    def __init__(self, status_code: int, body: object) -> None:
        data = body if isinstance(body, dict) else {"error": body}
        super().__init__(data)
        self.status_code = status_code
        self.body = body

    def json(self) -> object:
        return self.body

    def close(self) -> None:
        pass

    async def aclose(self) -> None:
        pass


class LoadBalancerResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LoadBalancerResourceWithRawResponse:
        """Return raw HTTP responses instead of parsed models."""
        return LoadBalancerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LoadBalancerResourceWithStreamingResponse:
        """Return streamed HTTP responses instead of eagerly reading them."""
        return LoadBalancerResourceWithStreamingResponse(self)

    def validate_region(self, x_region: str) -> None:
        if not x_region.strip():
            raise ValueError("'x_region' must be a non-empty string.")
        if x_region not in SUPPORTED_REGIONS:
            raise unsupported_region_error()

    def _headers(
        self,
        *,
        k_customer_id: str | None,
        x_account_id: str | None,
        x_region: str,
        extra_headers: Headers | None,
    ) -> Headers:
        self.validate_region(x_region)
        headers: dict[str, str] = {
            "Accept": "*/*",
            "x-region": x_region,
        }
        if k_customer_id is not None:
            headers["k-customer-id"] = k_customer_id
        if x_account_id is not None:
            headers["x-account-id"] = x_account_id
        return {**headers, **(extra_headers or {})}

    def create_target_group(
        self,
        *,
        target_group_name: str,
        vpc_krn: str,
        members: Iterable[create_target_group_params.Member],
        health_monitor: create_target_group_params.HealthMonitor,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        lb_krn: Iterable[str] = (),
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateTargetGroupResponse:
        """Create a target group and its health monitor and members."""
        headers = self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        try:
            return self._post(
                "/api/v3/loadBalancer/targetgroup",
                body=maybe_transform(
                    {
                        "target_group_name": target_group_name,
                        "vpc_krn": vpc_krn,
                        "lb_krn": lb_krn,
                        "members": members,
                        "health_monitor": health_monitor,
                    },
                    create_target_group_params.CreateTargetGroupParams,
                ),
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=CreateTargetGroupResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    def list_target_groups(
        self,
        *,
        vpc_krn: str,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListTargetGroupsResponse:
        """List target groups in a VPC."""
        headers = self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        try:
            return self._get(
                "/api/v3/loadBalancer/targetgroups",
                options=make_request_options(
                    query={"vpc_krn": vpc_krn},
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=ListTargetGroupsResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    def update_target_group(
        self,
        target_group_krn: str,
        *,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        members: Iterable[update_target_group_params.Member] | Omit = omit,
        health_monitor: update_target_group_params.HealthMonitor | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UpdateTargetGroupResponse:
        """Update the members and health monitor of a target group."""
        if not target_group_krn:
            raise ValueError("'target_group_krn' must be a non-empty string.")
        headers = self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        encoded_krn = quote(target_group_krn, safe="")
        try:
            return self._put(
                f"/api/v3/loadBalancer/targetgroup/{encoded_krn}",
                body=maybe_transform(
                    {
                        "krn": target_group_krn,
                        "members": members,
                        "health_monitor": health_monitor,
                    },
                    update_target_group_params.UpdateTargetGroupParams,
                ),
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=UpdateTargetGroupResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    def delete_target_group(
        self,
        target_group_krn: str,
        *,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteTargetGroupResponse:
        """Delete a target group by KRN."""
        if not target_group_krn:
            raise ValueError("'target_group_krn' must be a non-empty string.")
        headers = self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        encoded_krn = quote(target_group_krn, safe="")
        try:
            return self._delete(
                f"/api/v3/loadBalancer/targetgroup/{encoded_krn}",
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=DeleteTargetGroupResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    def create_load_balancer(
        self,
        *,
        loadbalancer_data: create_load_balancer_params.LoadBalancerData,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateLoadBalancerResponse:
        """Create a load balancer with listeners, pools, policies, and rules."""
        headers = self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        try:
            return self._post(
                "/api/v3/loadbalancer",
                body=maybe_transform(
                    {"loadbalancer_data": loadbalancer_data},
                    create_load_balancer_params.CreateLoadBalancerParams,
                ),
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=CreateLoadBalancerResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    def list_load_balancers_by_vpc(
        self,
        *,
        vpc_krn: str,
        x_region: str,
        k_customer_id: str | None = None,
        x_account_id: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListLoadBalancersResponse:
        """List load balancers in a VPC with pagination."""
        if page is not None and page < 1:
            raise ValueError("'page' must be greater than or equal to 1.")
        if limit is not None and limit < 1:
            raise ValueError("'limit' must be greater than or equal to 1.")
        headers = self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        query: dict[str, object] = {"vpc_krn": vpc_krn}
        if page is not None:
            query["page"] = page
        if limit is not None:
            query["limit"] = limit
        try:
            return self._get(
                "/api/v3/loadbalancer/getallbyvpc",
                options=make_request_options(
                    query=query,
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=ListLoadBalancersResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    def update_load_balancer(
        self,
        lb_krn: str,
        *,
        x_region: str,
        listener_krn: str | Omit = omit,
        listener: update_load_balancer_params.ListenerUpdate | Omit = omit,
        loadbalancer: update_load_balancer_params.LoadBalancerUpdate | Omit = omit,
        policy: Iterable[update_load_balancer_params.PolicyOperation] | Omit = omit,
        rules: Iterable[update_load_balancer_params.RuleOperation] | Omit = omit,
        pool: Iterable[update_load_balancer_params.PoolUpdate] | Omit = omit,
        k_customer_id: str | None = None,
        x_account_id: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Update load-balancer components in a single operation."""
        if not lb_krn:
            raise ValueError("'lb_krn' must be a non-empty string.")
        headers = self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        try:
            return self._put(
                f"/api/v3/loadbalancer/{lb_krn}",
                body=maybe_transform(
                    {
                        "loadbalancer_krn": lb_krn,
                        "listener_krn": listener_krn,
                        "listener": listener,
                        "loadbalancer": loadbalancer,
                        "policy": policy,
                        "rules": rules,
                        "pool": pool,
                    },
                    update_load_balancer_params.UpdateLoadBalancerParams,
                ),
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=object,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    def delete_load_balancer(
        self,
        lb_krn: str,
        *,
        x_region: str,
        k_customer_id: str | None = None,
        x_account_id: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Delete a load balancer by KRN."""
        if not lb_krn:
            raise ValueError("'lb_krn' must be a non-empty string.")
        headers = self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        try:
            return self._delete(
                f"/api/v3/loadbalancer/{lb_krn}",
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=NoneType,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)


class AsyncLoadBalancerResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLoadBalancerResourceWithRawResponse:
        """Return raw HTTP responses instead of parsed models."""
        return AsyncLoadBalancerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLoadBalancerResourceWithStreamingResponse:
        """Return streamed HTTP responses instead of eagerly reading them."""
        return AsyncLoadBalancerResourceWithStreamingResponse(self)

    async def validate_region(self, x_region: str) -> None:
        if not x_region.strip():
            raise ValueError("'x_region' must be a non-empty string.")
        if x_region not in SUPPORTED_REGIONS:
            raise unsupported_region_error()

    async def _headers(
        self,
        *,
        k_customer_id: str | None,
        x_account_id: str | None,
        x_region: str,
        extra_headers: Headers | None,
    ) -> Headers:
        await self.validate_region(x_region)
        headers: dict[str, str] = {
            "Accept": "*/*",
            "x-region": x_region,
        }
        if k_customer_id is not None:
            headers["k-customer-id"] = k_customer_id
        if x_account_id is not None:
            headers["x-account-id"] = x_account_id
        return {**headers, **(extra_headers or {})}

    async def create_target_group(
        self,
        *,
        target_group_name: str,
        vpc_krn: str,
        members: Iterable[create_target_group_params.Member],
        health_monitor: create_target_group_params.HealthMonitor,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        lb_krn: Iterable[str] = (),
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateTargetGroupResponse:
        """Create a target group and its health monitor and members."""
        headers = await self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        try:
            return await self._post(
                "/api/v3/loadBalancer/targetgroup",
                body=await async_maybe_transform(
                    {
                        "target_group_name": target_group_name,
                        "vpc_krn": vpc_krn,
                        "lb_krn": lb_krn,
                        "members": members,
                        "health_monitor": health_monitor,
                    },
                    create_target_group_params.CreateTargetGroupParams,
                ),
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=CreateTargetGroupResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    async def list_target_groups(
        self,
        *,
        vpc_krn: str,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListTargetGroupsResponse:
        """List target groups in a VPC."""
        headers = await self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        try:
            return await self._get(
                "/api/v3/loadBalancer/targetgroups",
                options=make_request_options(
                    query={"vpc_krn": vpc_krn},
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=ListTargetGroupsResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    async def update_target_group(
        self,
        target_group_krn: str,
        *,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        members: Iterable[update_target_group_params.Member] | Omit = omit,
        health_monitor: update_target_group_params.HealthMonitor | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UpdateTargetGroupResponse:
        """Update the members and health monitor of a target group."""
        if not target_group_krn:
            raise ValueError("'target_group_krn' must be a non-empty string.")
        headers = await self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        encoded_krn = quote(target_group_krn, safe="")
        try:
            return await self._put(
                f"/api/v3/loadBalancer/targetgroup/{encoded_krn}",
                body=await async_maybe_transform(
                    {
                        "krn": target_group_krn,
                        "members": members,
                        "health_monitor": health_monitor,
                    },
                    update_target_group_params.UpdateTargetGroupParams,
                ),
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=UpdateTargetGroupResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    async def delete_target_group(
        self,
        target_group_krn: str,
        *,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeleteTargetGroupResponse:
        """Delete a target group by KRN."""
        if not target_group_krn:
            raise ValueError("'target_group_krn' must be a non-empty string.")
        headers = await self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        encoded_krn = quote(target_group_krn, safe="")
        try:
            return await self._delete(
                f"/api/v3/loadBalancer/targetgroup/{encoded_krn}",
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=DeleteTargetGroupResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    async def create_load_balancer(
        self,
        *,
        loadbalancer_data: create_load_balancer_params.LoadBalancerData,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateLoadBalancerResponse:
        """Create a load balancer with listeners, pools, policies, and rules."""
        headers = await self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        try:
            return await self._post(
                "/api/v3/loadbalancer",
                body=await async_maybe_transform(
                    {"loadbalancer_data": loadbalancer_data},
                    create_load_balancer_params.CreateLoadBalancerParams,
                ),
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=CreateLoadBalancerResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    async def list_load_balancers_by_vpc(
        self,
        *,
        vpc_krn: str,
        x_region: str,
        k_customer_id: str | None = None,
        x_account_id: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListLoadBalancersResponse:
        """List load balancers in a VPC with pagination."""
        if page is not None and page < 1:
            raise ValueError("'page' must be greater than or equal to 1.")
        if limit is not None and limit < 1:
            raise ValueError("'limit' must be greater than or equal to 1.")
        headers = await self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        query: dict[str, object] = {"vpc_krn": vpc_krn}
        if page is not None:
            query["page"] = page
        if limit is not None:
            query["limit"] = limit
        try:
            return await self._get(
                "/api/v3/loadbalancer/getallbyvpc",
                options=make_request_options(
                    query=query,
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=ListLoadBalancersResponse,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    async def update_load_balancer(
        self,
        lb_krn: str,
        *,
        x_region: str,
        listener_krn: str | Omit = omit,
        listener: update_load_balancer_params.ListenerUpdate | Omit = omit,
        loadbalancer: update_load_balancer_params.LoadBalancerUpdate | Omit = omit,
        policy: Iterable[update_load_balancer_params.PolicyOperation] | Omit = omit,
        rules: Iterable[update_load_balancer_params.RuleOperation] | Omit = omit,
        pool: Iterable[update_load_balancer_params.PoolUpdate] | Omit = omit,
        k_customer_id: str | None = None,
        x_account_id: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Update load-balancer components in a single operation."""
        if not lb_krn:
            raise ValueError("'lb_krn' must be a non-empty string.")
        headers = await self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        try:
            return await self._put(
                f"/api/v3/loadbalancer/{lb_krn}",
                body=await async_maybe_transform(
                    {
                        "loadbalancer_krn": lb_krn,
                        "listener_krn": listener_krn,
                        "listener": listener,
                        "loadbalancer": loadbalancer,
                        "policy": policy,
                        "rules": rules,
                        "pool": pool,
                    },
                    update_load_balancer_params.UpdateLoadBalancerParams,
                ),
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=object,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)

    async def delete_load_balancer(
        self,
        lb_krn: str,
        *,
        x_region: str,
        k_customer_id: str | None = None,
        x_account_id: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Delete a load balancer by KRN."""
        if not lb_krn:
            raise ValueError("'lb_krn' must be a non-empty string.")
        headers = await self._headers(
            k_customer_id=k_customer_id,
            x_account_id=x_account_id,
            x_region=x_region,
            extra_headers=extra_headers,
        )
        try:
            return await self._delete(
                f"/api/v3/loadbalancer/{lb_krn}",
                options=make_request_options(
                    extra_headers=headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                ),
                cast_to=NoneType,
            )
        except APIStatusError as e:
            return LoadBalancerErrorResponse(e.status_code, e.body)


class LoadBalancerResourceWithRawResponse:
    def __init__(self, load_balancer: LoadBalancerResource) -> None:
        self._load_balancer = load_balancer
        self.create_target_group = to_raw_response_wrapper(load_balancer.create_target_group)
        self.list_target_groups = to_raw_response_wrapper(load_balancer.list_target_groups)
        self.update_target_group = to_raw_response_wrapper(load_balancer.update_target_group)
        self.delete_target_group = to_raw_response_wrapper(load_balancer.delete_target_group)
        self.create_load_balancer = to_raw_response_wrapper(load_balancer.create_load_balancer)
        self.list_load_balancers_by_vpc = to_raw_response_wrapper(load_balancer.list_load_balancers_by_vpc)
        self.update_load_balancer = to_raw_response_wrapper(load_balancer.update_load_balancer)
        self.delete_load_balancer = to_raw_response_wrapper(load_balancer.delete_load_balancer)


class AsyncLoadBalancerResourceWithRawResponse:
    def __init__(self, load_balancer: AsyncLoadBalancerResource) -> None:
        self._load_balancer = load_balancer
        self.create_target_group = async_to_raw_response_wrapper(load_balancer.create_target_group)
        self.list_target_groups = async_to_raw_response_wrapper(load_balancer.list_target_groups)
        self.update_target_group = async_to_raw_response_wrapper(load_balancer.update_target_group)
        self.delete_target_group = async_to_raw_response_wrapper(load_balancer.delete_target_group)
        self.create_load_balancer = async_to_raw_response_wrapper(load_balancer.create_load_balancer)
        self.list_load_balancers_by_vpc = async_to_raw_response_wrapper(load_balancer.list_load_balancers_by_vpc)
        self.update_load_balancer = async_to_raw_response_wrapper(load_balancer.update_load_balancer)
        self.delete_load_balancer = async_to_raw_response_wrapper(load_balancer.delete_load_balancer)


class LoadBalancerResourceWithStreamingResponse:
    def __init__(self, load_balancer: LoadBalancerResource) -> None:
        self._load_balancer = load_balancer
        self.create_target_group = to_streamed_response_wrapper(load_balancer.create_target_group)
        self.list_target_groups = to_streamed_response_wrapper(load_balancer.list_target_groups)
        self.update_target_group = to_streamed_response_wrapper(load_balancer.update_target_group)
        self.delete_target_group = to_streamed_response_wrapper(load_balancer.delete_target_group)
        self.create_load_balancer = to_streamed_response_wrapper(load_balancer.create_load_balancer)
        self.list_load_balancers_by_vpc = to_streamed_response_wrapper(load_balancer.list_load_balancers_by_vpc)
        self.update_load_balancer = to_streamed_response_wrapper(load_balancer.update_load_balancer)
        self.delete_load_balancer = to_streamed_response_wrapper(load_balancer.delete_load_balancer)


class AsyncLoadBalancerResourceWithStreamingResponse:
    def __init__(self, load_balancer: AsyncLoadBalancerResource) -> None:
        self._load_balancer = load_balancer
        self.create_target_group = async_to_streamed_response_wrapper(load_balancer.create_target_group)
        self.list_target_groups = async_to_streamed_response_wrapper(load_balancer.list_target_groups)
        self.update_target_group = async_to_streamed_response_wrapper(load_balancer.update_target_group)
        self.delete_target_group = async_to_streamed_response_wrapper(load_balancer.delete_target_group)
        self.create_load_balancer = async_to_streamed_response_wrapper(load_balancer.create_load_balancer)
        self.list_load_balancers_by_vpc = async_to_streamed_response_wrapper(load_balancer.list_load_balancers_by_vpc)
        self.update_load_balancer = async_to_streamed_response_wrapper(load_balancer.update_load_balancer)
        self.delete_load_balancer = async_to_streamed_response_wrapper(load_balancer.delete_load_balancer)


HighlvlResource = LoadBalancerResource
AsyncHighlvlResource = AsyncLoadBalancerResource
HighlvlResourceWithRawResponse = LoadBalancerResourceWithRawResponse
AsyncHighlvlResourceWithRawResponse = AsyncLoadBalancerResourceWithRawResponse
HighlvlResourceWithStreamingResponse = LoadBalancerResourceWithStreamingResponse
AsyncHighlvlResourceWithStreamingResponse = AsyncLoadBalancerResourceWithStreamingResponse

