from __future__ import annotations

import json
from typing import Any, Callable

import httpx
import pytest

from krutrim_client import KrutrimClient, AsyncKrutrimClient, _client as client_module
from krutrim_client._regions import SUPPORTED_REGIONS
from krutrim_client.types.kks.clusters.node_group_update_config_params import ScalingConfig

CLUSTER_KRN = "krn:kks:In-Hyderabad-2:account:customer:cluster:cluster-id"
NODEGROUP_KRN = "krn:kks:In-Hyderabad-2:account:customer:nodegroup:nodegroup-id"
KUBECONFIG = "apiVersion: v1\nkind: Config\nclusters: []\ncontexts: []\nusers: []\n"
MODES = ("parsed", "raw", "streaming")


@pytest.fixture(autouse=True)
def clear_region_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KRUTRIM_REGION", raising=False)
    monkeypatch.delenv("REGION", raising=False)
    monkeypatch.setattr(client_module, "_DOTENV_LOADED", True)


def make_client(handler: Callable[[httpx.Request], httpx.Response], *, region: str | None = None) -> KrutrimClient:
    return KrutrimClient(
        api_key="test-key",
        base_url="https://kks.test",
        region=region,
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        _strict_response_validation=True,
    )


def make_async_client(
    handler: Callable[[httpx.Request], httpx.Response], *, region: str | None = None
) -> AsyncKrutrimClient:
    client = AsyncKrutrimClient(
        api_key="test-key",
        base_url="https://kks.test",
        region=region,
        max_retries=0,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        _strict_response_validation=True,
    )
    client._platform = "Linux"
    return client


@pytest.mark.parametrize("region", [None, *SUPPORTED_REGIONS])
@pytest.mark.parametrize("mode", MODES)
def test_list_clusters(region: str | None, mode: str) -> None:
    body = {"clusters": [{"name": "test", "krn": CLUSTER_KRN}]}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/v1/kks/clusters"
        assert request.url.params.get("region") == region
        assert request.headers.get("x-region") == region
        return httpx.Response(200, json=body)

    with make_client(handler) as client:
        if mode == "raw":
            assert client.kks.clusters.with_raw_response.list(region=region).parse() == body
        elif mode == "streaming":
            with client.kks.clusters.with_streaming_response.list(region=region) as response:
                assert response.parse() == body
        else:
            assert client.kks.clusters.list(region=region) == body


@pytest.mark.parametrize("region", [None, *SUPPORTED_REGIONS])
@pytest.mark.parametrize("mode", MODES)
async def test_async_list_clusters(region: str | None, mode: str) -> None:
    body = {"clusters": [{"name": "test", "krn": CLUSTER_KRN}]}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/v1/kks/clusters"
        assert request.url.params.get("region") == region
        assert request.headers.get("x-region") == region
        return httpx.Response(200, json=body)

    async with make_async_client(handler) as client:
        if mode == "raw":
            response = await client.kks.clusters.with_raw_response.list(region=region)
            assert await response.parse() == body
        elif mode == "streaming":
            async with client.kks.clusters.with_streaming_response.list(region=region) as response:
                assert await response.parse() == body
        else:
            assert await client.kks.clusters.list(region=region) == body


@pytest.mark.parametrize("region", [None, "In-Bangalore-1"])
def test_list_clusters_client_region_and_request_options(region: str | None) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        expected_region = region or "In-Hyderabad-2"
        assert request.url.params == httpx.QueryParams(region=expected_region, limit=10)
        assert request.headers["x-region"] == expected_region
        assert request.headers["x-test"] == "value"
        assert request.extensions["timeout"]["read"] == 7
        return httpx.Response(200, json={"clusters": []})

    with make_client(handler, region="In-Hyderabad-2") as client:
        assert client.kks.clusters.list(
            region=region, extra_query={"limit": 10}, extra_headers={"x-test": "value"}, timeout=7
        ) == {"clusters": []}


@pytest.mark.parametrize("region", [None, "In-Bangalore-1"])
async def test_async_list_clusters_client_region_and_request_options(region: str | None) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        expected_region = region or "In-Hyderabad-2"
        assert request.url.params == httpx.QueryParams(region=expected_region, limit=10)
        assert request.headers["x-region"] == expected_region
        assert request.headers["x-test"] == "value"
        assert request.extensions["timeout"]["read"] == 7
        return httpx.Response(200, json={"clusters": []})

    async with make_async_client(handler, region="In-Hyderabad-2") as client:
        assert await client.kks.clusters.list(
            region=region, extra_query={"limit": 10}, extra_headers={"x-test": "value"}, timeout=7
        ) == {"clusters": []}


@pytest.mark.parametrize("region", ["", "In-Delhi-1"])
async def test_list_clusters_rejects_invalid_region(region: str) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        pytest.fail(f"Unexpected request: {request.url}")

    with make_client(handler) as client:
        with pytest.raises(ValueError, match="region"):
            client.kks.clusters.list(region=region)
    async with make_async_client(handler) as async_client:
        with pytest.raises(ValueError, match="region"):
            await async_client.kks.clusters.list(region=region)


@pytest.mark.parametrize(
    "content_type", [None, "application/yaml", "text/plain", "application/octet-stream", "application/json"]
)
@pytest.mark.parametrize("mode", MODES)
def test_retrieve_kubeconfig(content_type: str | None, mode: str) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == f"/v1/kks/clusters/{CLUSTER_KRN}/kubeconfig"
        headers = {"content-type": content_type} if content_type else {}
        return httpx.Response(200, content=KUBECONFIG.encode(), headers=headers)

    with make_client(handler) as client:
        if mode == "raw":
            response = client.kks.clusters.with_raw_response.retrieve_kubeconfig(CLUSTER_KRN)
            assert response.text() == KUBECONFIG
            assert response.parse() == KUBECONFIG
        elif mode == "streaming":
            with client.kks.clusters.with_streaming_response.retrieve_kubeconfig(CLUSTER_KRN) as response:
                assert response.parse() == KUBECONFIG
        else:
            assert client.kks.clusters.retrieve_kubeconfig(CLUSTER_KRN) == KUBECONFIG


@pytest.mark.parametrize(
    "content_type", [None, "application/yaml", "text/plain", "application/octet-stream", "application/json"]
)
@pytest.mark.parametrize("mode", MODES)
async def test_async_retrieve_kubeconfig(content_type: str | None, mode: str) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == f"/v1/kks/clusters/{CLUSTER_KRN}/kubeconfig"
        headers = {"content-type": content_type} if content_type else {}
        return httpx.Response(200, content=KUBECONFIG.encode(), headers=headers)

    async with make_async_client(handler) as client:
        if mode == "raw":
            response = await client.kks.clusters.with_raw_response.retrieve_kubeconfig(CLUSTER_KRN)
            assert await response.text() == KUBECONFIG
            assert await response.parse() == KUBECONFIG
        elif mode == "streaming":
            async with client.kks.clusters.with_streaming_response.retrieve_kubeconfig(CLUSTER_KRN) as response:
                assert await response.parse() == KUBECONFIG
        else:
            assert await client.kks.clusters.retrieve_kubeconfig(CLUSTER_KRN) == KUBECONFIG


def update_config_handler(request: httpx.Request) -> httpx.Response:
    assert request.method == "POST"
    assert request.url.path == f"/v1/kks/clusters/{CLUSTER_KRN}/node-groups/{NODEGROUP_KRN}/update-config"
    assert json.loads(request.content) == {
        "scalingConfig": {"minSize": 2, "maxSize": 5, "desiredSize": 4},
        "custom": True,
    }
    assert request.headers["x-region"] == "In-Hyderabad-2"
    assert request.url.params["custom"] == "true"
    assert request.extensions["timeout"]["read"] == 7
    return httpx.Response(200, json={"status": "UPDATING"})


@pytest.mark.parametrize("mode", MODES)
def test_update_config(mode: str) -> None:
    with make_client(update_config_handler, region="In-Hyderabad-2") as client:
        resource: Any = client.kks.clusters.node_groups
        if mode == "raw":
            resource = resource.with_raw_response
        elif mode == "streaming":
            resource = resource.with_streaming_response
        result = resource.update_config(
            NODEGROUP_KRN,
            cluster_krn=CLUSTER_KRN,
            scaling_config={"min_size": 2, "max_size": 5, "desired_size": 4},
            extra_query={"custom": True},
            extra_body={"custom": True},
            timeout=7,
        )
        if mode == "raw":
            result = result.parse()
        elif mode == "streaming":
            with result as response:
                result = response.parse()
        assert result == {"status": "UPDATING"}


@pytest.mark.parametrize("mode", MODES)
async def test_async_update_config(mode: str) -> None:
    async with make_async_client(update_config_handler, region="In-Hyderabad-2") as client:
        resource: Any = client.kks.clusters.node_groups
        if mode == "raw":
            resource = resource.with_raw_response
        elif mode == "streaming":
            resource = resource.with_streaming_response
        result = resource.update_config(
            NODEGROUP_KRN,
            cluster_krn=CLUSTER_KRN,
            scaling_config={"min_size": 2, "max_size": 5, "desired_size": 4},
            extra_query={"custom": True},
            extra_body={"custom": True},
            timeout=7,
        )
        if mode == "streaming":
            async with result as response:
                result = await response.parse()
        else:
            result = await result
            if mode == "raw":
                result = await result.parse()
        assert result == {"status": "UPDATING"}


@pytest.mark.parametrize("invalid_parameter", ["cluster_krn", "nodegroup_krn", "scaling_config"])
async def test_update_config_rejects_empty_parameters(invalid_parameter: str) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        pytest.fail(f"Unexpected request: {request.url}")

    cluster_krn = "" if invalid_parameter == "cluster_krn" else CLUSTER_KRN
    nodegroup_krn = "" if invalid_parameter == "nodegroup_krn" else NODEGROUP_KRN
    scaling_config: ScalingConfig = {} if invalid_parameter == "scaling_config" else {"desired_size": 4}
    with make_client(handler) as client:
        with pytest.raises(ValueError, match=invalid_parameter):
            client.kks.clusters.node_groups.update_config(
                nodegroup_krn, cluster_krn=cluster_krn, scaling_config=scaling_config
            )
    async with make_async_client(handler) as async_client:
        with pytest.raises(ValueError, match=invalid_parameter):
            await async_client.kks.clusters.node_groups.update_config(
                nodegroup_krn, cluster_krn=cluster_krn, scaling_config=scaling_config
            )
