# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, NOT_GIVEN
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.kks.clusters import node_group_create_params, node_group_upgrade_params
from typing import Optional

__all__ = ["NodeGroupsResource", "AsyncNodeGroupsResource"]


class NodeGroupsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NodeGroupsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/kks-python#accessing-raw-response-data-eg-headers
        """
        return NodeGroupsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NodeGroupsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/kks-python#with_streaming_response
        """
        return NodeGroupsResourceWithStreamingResponse(self)

    def create(
        self,
        cluster_krn: str,
        *,
        disk_size: int | Omit = omit,
        instance_types: str | Omit = omit,
        name: str | Omit = omit,
        node_repair_config: object | Omit = omit,
        remote_access: object | Omit = omit,
        scaling_config: object | Omit = omit,
        subnets_krn: str | Omit = omit,
        labels: Optional[object] = None,  # optional object
        taints: Optional[object] = None,  # optional object
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Nodegroup

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/v1/kks/clusters/{cluster_krn}/node-groups",
            body=maybe_transform(
                {
                    "disk_size": disk_size,
                    "instance_types": instance_types,
                    "name": name,
                    "node_repair_config": node_repair_config,
                    "remote_access": remote_access,
                    "scaling_config": scaling_config,
                    "subnets_krn": subnets_krn,
                    "labels": labels,   
                    "taints": taints,   
                },
                node_group_create_params.NodeGroupCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def retrieve(
        self,
        nodegroup_krn: str,
        *,
        cluster_krn: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        GET Nodegroup Details

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        if not nodegroup_krn:
            raise ValueError(f"Expected a non-empty value for `nodegroup_krn` but received {nodegroup_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/v1/kks/clusters/{cluster_krn}/node-groups/{nodegroup_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list(
        self,
        cluster_krn: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        List All NodeGroups

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/v1/kks/clusters/{cluster_krn}/node-groups",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def delete(
        self,
        nodegroup_krn: str,
        *,
        cluster_krn: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Nodegroup

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        if not nodegroup_krn:
            raise ValueError(f"Expected a non-empty value for `nodegroup_krn` but received {nodegroup_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/v1/kks/clusters/{cluster_krn}/node-groups/{nodegroup_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def upgrade(
        self,
        nodegroup_krn: str,
        *,
        cluster_krn: str,
        scaling_config: node_group_upgrade_params.ScalingConfig | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Upgrade nodegroup

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        if not nodegroup_krn:
            raise ValueError(f"Expected a non-empty value for `nodegroup_krn` but received {nodegroup_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._put(
            f"/v1/kks/clusters/{cluster_krn}/node-groups/{nodegroup_krn}",
            body=maybe_transform({"scaling_config": scaling_config}, node_group_upgrade_params.NodeGroupUpgradeParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncNodeGroupsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNodeGroupsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/kks-python#accessing-raw-response-data-eg-headers
        """
        return AsyncNodeGroupsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNodeGroupsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/kks-python#with_streaming_response
        """
        return AsyncNodeGroupsResourceWithStreamingResponse(self)

    async def create(
        self,
        cluster_krn: str,
        *,
        disk_size: int | Omit = omit,
        instance_types: str | Omit = omit,
        name: str | Omit = omit,
        node_repair_config: node_group_create_params.NodeRepairConfig | Omit = omit,
        remote_access: node_group_create_params.RemoteAccess | Omit = omit,
        scaling_config: node_group_create_params.ScalingConfig | Omit = omit,
        subnets_krn: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Nodegroup

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/v1/kks/clusters/{cluster_krn}/node-groups",
            body=await async_maybe_transform(
                {
                    "disk_size": disk_size,
                    "instance_types": instance_types,
                    "name": name,
                    "node_repair_config": node_repair_config,
                    "remote_access": remote_access,
                    "scaling_config": scaling_config,
                    "subnets_krn": subnets_krn,
                },
                node_group_create_params.NodeGroupCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def retrieve(
        self,
        nodegroup_krn: str,
        *,
        cluster_krn: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        GET Nodegroup Details

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        if not nodegroup_krn:
            raise ValueError(f"Expected a non-empty value for `nodegroup_krn` but received {nodegroup_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/v1/kks/clusters/{cluster_krn}/node-groups/{nodegroup_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def list(
        self,
        cluster_krn: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        List All NodeGroups

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/v1/kks/clusters/{cluster_krn}/node-groups",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def delete(
        self,
        nodegroup_krn: str,
        *,
        cluster_krn: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Nodegroup

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        if not nodegroup_krn:
            raise ValueError(f"Expected a non-empty value for `nodegroup_krn` but received {nodegroup_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/v1/kks/clusters/{cluster_krn}/node-groups/{nodegroup_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def upgrade(
        self,
        nodegroup_krn: str,
        *,
        cluster_krn: str,
        scaling_config: node_group_upgrade_params.ScalingConfig | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Upgrade nodegroup

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        if not nodegroup_krn:
            raise ValueError(f"Expected a non-empty value for `nodegroup_krn` but received {nodegroup_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._put(
            f"/v1/kks/clusters/{cluster_krn}/node-groups/{nodegroup_krn}",
            body=await async_maybe_transform(
                {"scaling_config": scaling_config}, node_group_upgrade_params.NodeGroupUpgradeParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class NodeGroupsResourceWithRawResponse:
    def __init__(self, node_groups: NodeGroupsResource) -> None:
        self._node_groups = node_groups

        self.create = to_raw_response_wrapper(
            node_groups.create,
        )
        self.retrieve = to_raw_response_wrapper(
            node_groups.retrieve,
        )
        self.list = to_raw_response_wrapper(
            node_groups.list,
        )
        self.delete = to_raw_response_wrapper(
            node_groups.delete,
        )
        self.upgrade = to_raw_response_wrapper(
            node_groups.upgrade,
        )


class AsyncNodeGroupsResourceWithRawResponse:
    def __init__(self, node_groups: AsyncNodeGroupsResource) -> None:
        self._node_groups = node_groups

        self.create = async_to_raw_response_wrapper(
            node_groups.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            node_groups.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            node_groups.list,
        )
        self.delete = async_to_raw_response_wrapper(
            node_groups.delete,
        )
        self.upgrade = async_to_raw_response_wrapper(
            node_groups.upgrade,
        )


class NodeGroupsResourceWithStreamingResponse:
    def __init__(self, node_groups: NodeGroupsResource) -> None:
        self._node_groups = node_groups

        self.create = to_streamed_response_wrapper(
            node_groups.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            node_groups.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            node_groups.list,
        )
        self.delete = to_streamed_response_wrapper(
            node_groups.delete,
        )
        self.upgrade = to_streamed_response_wrapper(
            node_groups.upgrade,
        )


class AsyncNodeGroupsResourceWithStreamingResponse:
    def __init__(self, node_groups: AsyncNodeGroupsResource) -> None:
        self._node_groups = node_groups

        self.create = async_to_streamed_response_wrapper(
            node_groups.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            node_groups.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            node_groups.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            node_groups.delete,
        )
        self.upgrade = async_to_streamed_response_wrapper(
            node_groups.upgrade,
        )
