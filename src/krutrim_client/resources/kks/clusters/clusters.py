# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .addons import (
    AddonsResource,
    AsyncAddonsResource,
    AddonsResourceWithRawResponse,
    AsyncAddonsResourceWithRawResponse,
    AddonsResourceWithStreamingResponse,
    AsyncAddonsResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, NOT_GIVEN
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from .node_groups import (
    NodeGroupsResource,
    AsyncNodeGroupsResource,
    NodeGroupsResourceWithRawResponse,
    AsyncNodeGroupsResourceWithRawResponse,
    NodeGroupsResourceWithStreamingResponse,
    AsyncNodeGroupsResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....types.kks import cluster_create_params, cluster_upgrade_params
from ...._base_client import make_request_options

__all__ = ["ClustersResource", "AsyncClustersResource"]


class ClustersResource(SyncAPIResource):
    @cached_property
    def node_groups(self) -> NodeGroupsResource:
        return NodeGroupsResource(self._client)

    @cached_property
    def addons(self) -> AddonsResource:
        return AddonsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ClustersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/kks-python#accessing-raw-response-data-eg-headers
        """
        return ClustersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ClustersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/kks-python#with_streaming_response
        """
        return ClustersResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        vpcKrn: str,
        subnetKrns: str,
        podIpv4Cidr: str,
        serviceIpv4Cidr:str,
        name: str | Omit = omit,
        version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Cluster

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/v1/kks/clusters",
            body=maybe_transform(
                {
                    "resourcesVpcConfig": {
                        "vpcKrn":vpcKrn,
                        "subnetKrns":subnetKrns
                    },
                    "name": name,
                    "kubernetesNetworkConfig": {
                        "podIpv4Cidr":podIpv4Cidr,
                        "serviceIpv4Cidr":serviceIpv4Cidr
                    },
                    "version": version,
                },
                cluster_create_params.ClusterCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def retrieve(
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
        Cluster by Cluster KRN

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
            f"/v1/kks/clusters/{cluster_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Get ALL clusters"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/v1/kks/clusters",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def delete(
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
        Delete cluster

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/v1/kks/clusters/{cluster_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def retrieve_kubeconfig(
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
        Retrieve kubeconfig

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
            f"/v1/kks/clusters/{cluster_krn}/kubeconfig",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def upgrade(
        self,
        cluster_krn: str,
        *,
        version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Upgrade cluster

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
            f"/v1/kks/clusters/{cluster_krn}/updates",
            body=maybe_transform({"version": version}, cluster_upgrade_params.ClusterUpgradeParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncClustersResource(AsyncAPIResource):
    @cached_property
    def node_groups(self) -> AsyncNodeGroupsResource:
        return AsyncNodeGroupsResource(self._client)

    @cached_property
    def addons(self) -> AsyncAddonsResource:
        return AsyncAddonsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncClustersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/kks-python#accessing-raw-response-data-eg-headers
        """
        return AsyncClustersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncClustersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/kks-python#with_streaming_response
        """
        return AsyncClustersResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        vpcKrn: str,
        subnetKrns: str,
        podIpv4Cidr: str,
        serviceIpv4Cidr:str,
        name: str | Omit = omit,
        version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Cluster

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/v1/kks/clusters",
            body=await async_maybe_transform(
                {
                    "resourcesVpcConfig": {
                        "vpcKrn":vpcKrn,
                        "subnetKrns":subnetKrns
                    },
                    "name": name,
                    "kubernetesNetworkConfig": {
                        "podIpv4Cidr":podIpv4Cidr,
                        "serviceIpv4Cidr":serviceIpv4Cidr
                    },
                    "version": version,
                },
                cluster_create_params.ClusterCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def retrieve(
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
        Cluster by Cluster KRN

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
            f"/v1/kks/clusters/{cluster_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Get ALL clusters"""
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/v1/kks/clusters",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def delete(
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
        Delete cluster

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not cluster_krn:
            raise ValueError(f"Expected a non-empty value for `cluster_krn` but received {cluster_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/v1/kks/clusters/{cluster_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def retrieve_kubeconfig(
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
        Retrieve kubeconfig

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
            f"/v1/kks/clusters/{cluster_krn}/kubeconfig",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def upgrade(
        self,
        cluster_krn: str,
        *,
        version: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Upgrade cluster

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
            f"/v1/kks/clusters/{cluster_krn}/updates",
            body=await async_maybe_transform({"version": version}, cluster_upgrade_params.ClusterUpgradeParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ClustersResourceWithRawResponse:
    def __init__(self, clusters: ClustersResource) -> None:
        self._clusters = clusters

        self.create = to_raw_response_wrapper(
            clusters.create,
        )
        self.retrieve = to_raw_response_wrapper(
            clusters.retrieve,
        )
        self.list = to_raw_response_wrapper(
            clusters.list,
        )
        self.delete = to_raw_response_wrapper(
            clusters.delete,
        )
        self.retrieve_kubeconfig = to_raw_response_wrapper(
            clusters.retrieve_kubeconfig,
        )
        self.upgrade = to_raw_response_wrapper(
            clusters.upgrade,
        )

    @cached_property
    def node_groups(self) -> NodeGroupsResourceWithRawResponse:
        return NodeGroupsResourceWithRawResponse(self._clusters.node_groups)

    @cached_property
    def addons(self) -> AddonsResourceWithRawResponse:
        return AddonsResourceWithRawResponse(self._clusters.addons)


class AsyncClustersResourceWithRawResponse:
    def __init__(self, clusters: AsyncClustersResource) -> None:
        self._clusters = clusters

        self.create = async_to_raw_response_wrapper(
            clusters.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            clusters.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            clusters.list,
        )
        self.delete = async_to_raw_response_wrapper(
            clusters.delete,
        )
        self.retrieve_kubeconfig = async_to_raw_response_wrapper(
            clusters.retrieve_kubeconfig,
        )
        self.upgrade = async_to_raw_response_wrapper(
            clusters.upgrade,
        )

    @cached_property
    def node_groups(self) -> AsyncNodeGroupsResourceWithRawResponse:
        return AsyncNodeGroupsResourceWithRawResponse(self._clusters.node_groups)

    @cached_property
    def addons(self) -> AsyncAddonsResourceWithRawResponse:
        return AsyncAddonsResourceWithRawResponse(self._clusters.addons)


class ClustersResourceWithStreamingResponse:
    def __init__(self, clusters: ClustersResource) -> None:
        self._clusters = clusters

        self.create = to_streamed_response_wrapper(
            clusters.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            clusters.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            clusters.list,
        )
        self.delete = to_streamed_response_wrapper(
            clusters.delete,
        )
        self.retrieve_kubeconfig = to_streamed_response_wrapper(
            clusters.retrieve_kubeconfig,
        )
        self.upgrade = to_streamed_response_wrapper(
            clusters.upgrade,
        )

    @cached_property
    def node_groups(self) -> NodeGroupsResourceWithStreamingResponse:
        return NodeGroupsResourceWithStreamingResponse(self._clusters.node_groups)

    @cached_property
    def addons(self) -> AddonsResourceWithStreamingResponse:
        return AddonsResourceWithStreamingResponse(self._clusters.addons)


class AsyncClustersResourceWithStreamingResponse:
    def __init__(self, clusters: AsyncClustersResource) -> None:
        self._clusters = clusters

        self.create = async_to_streamed_response_wrapper(
            clusters.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            clusters.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            clusters.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            clusters.delete,
        )
        self.retrieve_kubeconfig = async_to_streamed_response_wrapper(
            clusters.retrieve_kubeconfig,
        )
        self.upgrade = async_to_streamed_response_wrapper(
            clusters.upgrade,
        )

    @cached_property
    def node_groups(self) -> AsyncNodeGroupsResourceWithStreamingResponse:
        return AsyncNodeGroupsResourceWithStreamingResponse(self._clusters.node_groups)

    @cached_property
    def addons(self) -> AsyncAddonsResourceWithStreamingResponse:
        return AsyncAddonsResourceWithStreamingResponse(self._clusters.addons)
