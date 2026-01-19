# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ...types.lb import (
    highlvl_get_full_tg_list_params,
    highlvl_get_tg_names_only_params,
    highlvl_create_target_group_params,
    highlvl_delete_target_group_params,
    highlvl_update_target_group_params,
    highlvl_update_load_balancer_params,
    highlvl_get_detailed_target_groups_params,
    highlvl_create_load_balancer_orchestration_params
)
from ...types.lb.highlvl_create_target_group_response import TargetGroupCreateResponse   
from ...types.lb.highlvl_create_lb_orchestration_response import LBOrchestrationResp


from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven,Omit, omit
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options

__all__ = ["HighlvlResource", "AsyncHighlvlResource"]


class HighlvlResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> HighlvlResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/lb2-python#accessing-raw-response-data-eg-headers
        """
        return HighlvlResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> HighlvlResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/lb2-python#with_streaming_response
        """
        return HighlvlResourceWithStreamingResponse(self)
    


    def validate_region(self, x_region: str) -> None:
        if not x_region.strip():
            raise ValueError("'x_region' must be a non-empty string.")
        if x_region not in ('In-Bangalore-1'):
            raise ValueError(
                f"Invalid region '{x_region}'. Supported regions are: 'In-Bangalore-1'."
            )

    def create_load_balancer_orchestration(
        self,
        *,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        listeners: Iterable[object] | Omit = omit,
        loadbalancer_data: object | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LBOrchestrationResp:
        """
        Create Load Balancer Orchestration

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_region(x_region)
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"k-customer-id": k_customer_id, "x-account-id": x_account_id, "x-region": x_region})
        return self._post(
            "/v3/highlvl/create_load_balancer_orchestration",
            body=maybe_transform(
                {
                    "listeners": listeners,
                    "loadbalancer_data": loadbalancer_data,
                },
                highlvl_create_load_balancer_orchestration_params.HighlvlCreateLoadBalancerOrchestrationParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LBOrchestrationResp,
        )

    def create_target_group(
        self,
        *,
        x_region: str,
        health_monitor: highlvl_create_target_group_params.HealthMonitor | Omit = omit,
        members: Iterable[highlvl_create_target_group_params.Member] | Omit = omit,
        target_group_name: str | Omit = omit,
        vpc_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TargetGroupCreateResponse:
        """
        Create Target Group

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_region(x_region)
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region})
        return self._post(
            "/v1/highlvl/create_target_group",
            body=maybe_transform(
                {
                    "health_monitor": health_monitor,
                    "members": members,
                    "target_group_name": target_group_name,
                    "vpc_id": vpc_id,
                },
                highlvl_create_target_group_params.HighlvlCreateTargetGroupParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TargetGroupCreateResponse,
        )

    def delete_load_balancer(
        self,
        lb_krn: str,
        *,
        x_region: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Load Balancer

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_region(x_region)
        if not lb_krn:
            raise ValueError(f"Expected a non-empty value for `lb_krn` but received {lb_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region})
        return self._delete(
            f"/v3/highlvl/loadbalancer/{lb_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def delete_target_group(
        self,
        *,
        target_group_name: str,
        vpc_id: str,
        x_region:str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Target Group

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_region(x_region)
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region})
        return self._delete(
            "/v1/highlvl/target_group",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "target_group_name": target_group_name,
                        "vpc_id": vpc_id,
                    },
                    highlvl_delete_target_group_params.HighlvlDeleteTargetGroupParams,
                ),
            ),
            cast_to=NoneType,
        )

    def fetch_payload_multiple(
        self,
        lb_krn: str,
        x_region:str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Fetch Detailed LB Payload

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_region(x_region)
        if not lb_krn:
            raise ValueError(f"Expected a non-empty value for `lb_krn` but received {lb_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region})
        return self._get(
            f"/v3/highlvl/fetch_payload_multiple/{lb_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get_detailed_target_groups(
        self,
        *,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        vpc_id: str,
        target_group_name: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        self.validate_region(x_region)
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update(
            {
                "k-customer-id": k_customer_id,
                "x-account-id": x_account_id,
                "x-region": x_region,
            }
        )

        return self._get(
            "/v1/highlvl/get_target_groups",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"vpc_id": vpc_id, "target_group_name": target_group_name},
                    highlvl_get_detailed_target_groups_params.HighlvlGetDetailedTargetGroupsParams,
                ),
            ),
            cast_to=NoneType,
        )


    def get_full_tg_list(
        self,
        *,
        vpc_id: str,
        x_region:str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get Full TG List

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_region(x_region)
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region})
        return self._get(
            "/v1/highlvl/get_tg_list",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"vpc_id": vpc_id}, highlvl_get_full_tg_list_params.HighlvlGetFullTgListParams),
            ),
            cast_to=NoneType,
        )

    def get_task_status(
        self,
        task_id: str,
        x_region:str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get Task Status

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_region(x_region)
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region}) 
        return self._get(
            f"/v3/highlvl/task_status/{task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def get_tg_names_only(
        self,
        *,
        vpc_id: str,
        x_region:str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get TG Names Only

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_region(x_region)
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region}) 
        return self._get(
            "/v1/highlvl/get_target_group_names",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"vpc_id": vpc_id}, highlvl_get_tg_names_only_params.HighlvlGetTgNamesOnlyParams),
            ),
            cast_to=NoneType,
        )

    def list_load_balancers_by_vpc(
        self,
        vpc_krn: str,
        x_region:str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        List Load Balancers by VPC

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_region(x_region)
        if not vpc_krn:
            raise ValueError(f"Expected a non-empty value for `vpc_krn` but received {vpc_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region}) 
        return self._get(
            f"/v3/highlvl/get_lb_list_new/{vpc_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def update_load_balancer(
        self,
        path_lb_krn: str,
        *,
        x_region: str,
        k_customer_id: str,
        x_account_id: str,
        listeners: Iterable[object] | Omit = omit,
        loadbalancer_data: object | Omit = omit,
        security_groups: Iterable[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Update Load Balancer

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_region(x_region)
        if not path_lb_krn:
            raise ValueError(f"Expected a non-empty value for `path_lb_krn` but received {path_lb_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"k-customer-id": k_customer_id, "x-account-id": x_account_id, "x-region": x_region})
        payload: dict = {
            "lb_krn": path_lb_krn,
        }
        if listeners is not omit:
            payload["listeners"] = listeners
        if loadbalancer_data is not omit:
            payload["loadbalancer_data"] = loadbalancer_data
        if security_groups is not omit:
            payload["security_groups"] = list(security_groups)               
        return self._post(
            f"/v3/highlvl/update_load_balancer/{path_lb_krn}",
            body=payload,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def update_target_group(
        self,
        *,
        x_region: str,
        k_customer_id: str,
        x_account_id: str,
        health_monitor: highlvl_update_target_group_params.HealthMonitor | Omit = omit,
        members: Iterable[highlvl_update_target_group_params.Member] | Omit = omit,
        target_group_name: str | Omit = omit,
        vpc_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Update Target Group Members/Health

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_region(x_region)
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update(
            {
                "k-customer-id": k_customer_id,
                "x-account-id": x_account_id,
                "x-region": x_region,
            }
        )
        return self._post(
            "/v1/highlvl/updatetg",
            body=maybe_transform(
                {
                    "health_monitor": health_monitor,
                    "members": members,
                    "target_group_name": target_group_name,
                    "vpc_id": vpc_id,
                },
                highlvl_update_target_group_params.HighlvlUpdateTargetGroupParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncHighlvlResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncHighlvlResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/lb2-python#accessing-raw-response-data-eg-headers
        """
        return AsyncHighlvlResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncHighlvlResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/lb2-python#with_streaming_response
        """
        return AsyncHighlvlResourceWithStreamingResponse(self)
    async def validate_region(x_region: str) -> None:
        if not isinstance(x_region, str) or not x_region.strip():
            raise ValueError("'x_region' must be a non-empty string.")
        if x_region not in ('In-Bangalore-1'):
            raise ValueError(
                f"Invalid region '{x_region}'. Supported regions are: 'In-Bangalore-1'."
            )

    async def create_load_balancer_orchestration(
        self,
        *,
        k_customer_id: str,
        x_account_id: str,
        x_region: str,
        listeners: Iterable[object] | Omit = omit,
        loadbalancer_data: object | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Load Balancer Orchestration

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await self.validate_region(x_region)
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"k-customer-id": k_customer_id, "x-account-id": x_account_id, "x-region": x_region})
        return await self._post(
            "/v3/highlvl/create_load_balancer_orchestration",
            body=await async_maybe_transform(
                {
                    "listeners": listeners,
                    "loadbalancer_data": loadbalancer_data,
                },
                highlvl_create_load_balancer_orchestration_params.HighlvlCreateLoadBalancerOrchestrationParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def create_target_group(
        self,
        *,
        x_region: str,
        health_monitor: highlvl_create_target_group_params.HealthMonitor | Omit = omit,
        members: Iterable[highlvl_create_target_group_params.Member] | Omit = omit,
        target_group_name: str | Omit = omit,
        vpc_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Target Group

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await self.validate_region(x_region)
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region})
        return await self._post(
            "/v1/highlvl/create_target_group",
            body=await async_maybe_transform(
                {
                    "health_monitor": health_monitor,
                    "members": members,
                    "target_group_name": target_group_name,
                    "vpc_id": vpc_id,
                },
                highlvl_create_target_group_params.HighlvlCreateTargetGroupParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def delete_load_balancer(
        self,
        lb_krn: str,
        *,
        x_region: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Load Balancer

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await self.validate_region(x_region)
        if not lb_krn:
            raise ValueError(f"Expected a non-empty value for `lb_krn` but received {lb_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region})
        return await self._delete(
            f"/v3/highlvl/loadbalancer/{lb_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def delete_target_group(
        self,
        *,
        target_group_name: str,
        vpc_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Target Group

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            "/v1/highlvl/target_group",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "target_group_name": target_group_name,
                        "vpc_id": vpc_id,
                    },
                    highlvl_delete_target_group_params.HighlvlDeleteTargetGroupParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def fetch_payload_multiple(
        self,
        lb_krn: str,
        x_region:str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Fetch Detailed LB Payload

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await self.validate_region(x_region)
        if not lb_krn:
            raise ValueError(f"Expected a non-empty value for `lb_krn` but received {lb_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region})
        return await self._get(
            f"/v3/highlvl/fetch_payload_multiple/{lb_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_detailed_target_groups(
        self,
        *,
        vpc_id: str,
        x_region:str,
        target_group_name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get Detailed Target Groups

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await self.validate_region(x_region)
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region}) 
        return await self._get(
            "/v1/highlvl/get_target_groups",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "vpc_id": vpc_id,
                        "target_group_name": target_group_name,
                    },
                    highlvl_get_detailed_target_groups_params.HighlvlGetDetailedTargetGroupsParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def get_full_tg_list(
        self,
        *,
        vpc_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get Full TG List

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/v1/highlvl/get_tg_list",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"vpc_id": vpc_id}, highlvl_get_full_tg_list_params.HighlvlGetFullTgListParams
                ),
            ),
            cast_to=NoneType,
        )

    async def get_task_status(
        self,
        task_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get Task Status

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/v3/highlvl/task_status/{task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_tg_names_only(
        self,
        *,
        vpc_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get TG Names Only

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/v1/highlvl/get_target_group_names",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"vpc_id": vpc_id}, highlvl_get_tg_names_only_params.HighlvlGetTgNamesOnlyParams
                ),
            ),
            cast_to=NoneType,
        )

    async def list_load_balancers_by_vpc(
        self,
        vpc_krn: str,
        x_region:str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        List Load Balancers by VPC

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await self.validate_region(x_region)
        if not vpc_krn:
            raise ValueError(f"Expected a non-empty value for `vpc_krn` but received {vpc_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region}) 
        return await self._get(
            f"/v3/highlvl/get_lb_list_new/{vpc_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def update_load_balancer(
        self,
        path_lb_krn: str,
        *,
        x_region: str,
        k_customer_id: str,
        x_account_id: str,
        listeners: Iterable[object] | Omit = omit,
        loadbalancer_data: object | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Update Load Balancer

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await self.validate_region(x_region)
        if not path_lb_krn:
            raise ValueError(f"Expected a non-empty value for `path_lb_krn` but received {path_lb_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"k-customer-id": k_customer_id, "x-account-id": x_account_id, "x-region": x_region})
        payload: dict = {
            "lb_krn": path_lb_krn,
        }
        if listeners is not omit:
            payload["listeners"] = listeners
        if loadbalancer_data is not omit:
            payload["loadbalancer_data"] = loadbalancer_data
        return await self._post(
            f"/v3/highlvl/update_load_balancer/{path_lb_krn}",
            body=payload,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def update_target_group(
        self,
        *,
        x_region: str,
        k_customer_id: str,
        x_account_id: str,
        health_monitor: highlvl_update_target_group_params.HealthMonitor | Omit = omit,
        members: Iterable[highlvl_update_target_group_params.Member] | Omit = omit,
        target_group_name: str | Omit = omit,
        vpc_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Update Target Group Members/Health

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        await self.validate_region(x_region)
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update(
            {
                "k-customer-id": k_customer_id,
                "x-account-id": x_account_id,
                "x-region": x_region,
            }
        )
        return await self._post(
            "/v1/highlvl/updatetg",
            body=await async_maybe_transform(
                {
                    "health_monitor": health_monitor,
                    "members": members,
                    "target_group_name": target_group_name,
                    "vpc_id": vpc_id,
                },
                highlvl_update_target_group_params.HighlvlUpdateTargetGroupParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class HighlvlResourceWithRawResponse:
    def __init__(self, highlvl: HighlvlResource) -> None:
        self._highlvl = highlvl

        self.create_load_balancer_orchestration = to_raw_response_wrapper(
            highlvl.create_load_balancer_orchestration,
        )
        self.create_target_group = to_raw_response_wrapper(
            highlvl.create_target_group,
        )
        self.delete_load_balancer = to_raw_response_wrapper(
            highlvl.delete_load_balancer,
        )
        self.delete_target_group = to_raw_response_wrapper(
            highlvl.delete_target_group,
        )
        self.fetch_payload_multiple = to_raw_response_wrapper(
            highlvl.fetch_payload_multiple,
        )
        self.get_detailed_target_groups = to_raw_response_wrapper(
            highlvl.get_detailed_target_groups,
        )
        self.get_full_tg_list = to_raw_response_wrapper(
            highlvl.get_full_tg_list,
        )
        self.get_task_status = to_raw_response_wrapper(
            highlvl.get_task_status,
        )
        self.get_tg_names_only = to_raw_response_wrapper(
            highlvl.get_tg_names_only,
        )
        self.list_load_balancers_by_vpc = to_raw_response_wrapper(
            highlvl.list_load_balancers_by_vpc,
        )
        self.update_load_balancer = to_raw_response_wrapper(
            highlvl.update_load_balancer,
        )
        self.update_target_group = to_raw_response_wrapper(
            highlvl.update_target_group,
        )


class AsyncHighlvlResourceWithRawResponse:
    def __init__(self, highlvl: AsyncHighlvlResource) -> None:
        self._highlvl = highlvl

        self.create_load_balancer_orchestration = async_to_raw_response_wrapper(
            highlvl.create_load_balancer_orchestration,
        )
        self.create_target_group = async_to_raw_response_wrapper(
            highlvl.create_target_group,
        )
        self.delete_load_balancer = async_to_raw_response_wrapper(
            highlvl.delete_load_balancer,
        )
        self.delete_target_group = async_to_raw_response_wrapper(
            highlvl.delete_target_group,
        )
        self.fetch_payload_multiple = async_to_raw_response_wrapper(
            highlvl.fetch_payload_multiple,
        )
        self.get_detailed_target_groups = async_to_raw_response_wrapper(
            highlvl.get_detailed_target_groups,
        )
        self.get_full_tg_list = async_to_raw_response_wrapper(
            highlvl.get_full_tg_list,
        )
        self.get_task_status = async_to_raw_response_wrapper(
            highlvl.get_task_status,
        )
        self.get_tg_names_only = async_to_raw_response_wrapper(
            highlvl.get_tg_names_only,
        )
        self.list_load_balancers_by_vpc = async_to_raw_response_wrapper(
            highlvl.list_load_balancers_by_vpc,
        )
        self.update_load_balancer = async_to_raw_response_wrapper(
            highlvl.update_load_balancer,
        )
        self.update_target_group = async_to_raw_response_wrapper(
            highlvl.update_target_group,
        )


class HighlvlResourceWithStreamingResponse:
    def __init__(self, highlvl: HighlvlResource) -> None:
        self._highlvl = highlvl

        self.create_load_balancer_orchestration = to_streamed_response_wrapper(
            highlvl.create_load_balancer_orchestration,
        )
        self.create_target_group = to_streamed_response_wrapper(
            highlvl.create_target_group,
        )
        self.delete_load_balancer = to_streamed_response_wrapper(
            highlvl.delete_load_balancer,
        )
        self.delete_target_group = to_streamed_response_wrapper(
            highlvl.delete_target_group,
        )
        self.fetch_payload_multiple = to_streamed_response_wrapper(
            highlvl.fetch_payload_multiple,
        )
        self.get_detailed_target_groups = to_streamed_response_wrapper(
            highlvl.get_detailed_target_groups,
        )
        self.get_full_tg_list = to_streamed_response_wrapper(
            highlvl.get_full_tg_list,
        )
        self.get_task_status = to_streamed_response_wrapper(
            highlvl.get_task_status,
        )
        self.get_tg_names_only = to_streamed_response_wrapper(
            highlvl.get_tg_names_only,
        )
        self.list_load_balancers_by_vpc = to_streamed_response_wrapper(
            highlvl.list_load_balancers_by_vpc,
        )
        self.update_load_balancer = to_streamed_response_wrapper(
            highlvl.update_load_balancer,
        )
        self.update_target_group = to_streamed_response_wrapper(
            highlvl.update_target_group,
        )


class AsyncHighlvlResourceWithStreamingResponse:
    def __init__(self, highlvl: AsyncHighlvlResource) -> None:
        self._highlvl = highlvl

        self.create_load_balancer_orchestration = async_to_streamed_response_wrapper(
            highlvl.create_load_balancer_orchestration,
        )
        self.create_target_group = async_to_streamed_response_wrapper(
            highlvl.create_target_group,
        )
        self.delete_load_balancer = async_to_streamed_response_wrapper(
            highlvl.delete_load_balancer,
        )
        self.delete_target_group = async_to_streamed_response_wrapper(
            highlvl.delete_target_group,
        )
        self.fetch_payload_multiple = async_to_streamed_response_wrapper(
            highlvl.fetch_payload_multiple,
        )
        self.get_detailed_target_groups = async_to_streamed_response_wrapper(
            highlvl.get_detailed_target_groups,
        )
        self.get_full_tg_list = async_to_streamed_response_wrapper(
            highlvl.get_full_tg_list,
        )
        self.get_task_status = async_to_streamed_response_wrapper(
            highlvl.get_task_status,
        )
        self.get_tg_names_only = async_to_streamed_response_wrapper(
            highlvl.get_tg_names_only,
        )
        self.list_load_balancers_by_vpc = async_to_streamed_response_wrapper(
            highlvl.list_load_balancers_by_vpc,
        )
        self.update_load_balancer = async_to_streamed_response_wrapper(
            highlvl.update_load_balancer,
        )
        self.update_target_group = async_to_streamed_response_wrapper(
            highlvl.update_target_group,
        )