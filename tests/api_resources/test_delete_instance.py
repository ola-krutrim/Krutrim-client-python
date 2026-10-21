from __future__ import annotations

import httpx
import pytest

from krutrim_client import KrutrimClient, AsyncKrutrimClient
from krutrim_client._regions import SUPPORTED_REGIONS


@pytest.mark.parametrize("region", SUPPORTED_REGIONS)
@pytest.mark.parametrize("delete_volume", [True, False])
@pytest.mark.parametrize("mode", ["parsed", "raw", "streaming"])
def test_delete_instance_uses_krn_region(region: str, delete_volume: bool, mode: str) -> None:
    instance_krn = f"krn:vm:{region}:account:customer:instance:instance-id"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        assert request.url.path == "/vm/v1/delete_instance_async"
        assert dict(request.url.params) == {"instanceKrn": instance_krn, "deleteVolume": str(delete_volume).lower()}
        assert request.headers["x-region"] == region
        assert request.headers["x-test"] == "value"
        assert request.extensions["timeout"]["read"] == 7
        return httpx.Response(202, json={"message": "Deletion started", "task_id": "task-id"})

    with KrutrimClient(
        api_key="test-key",
        base_url="https://vm.test",
        region="In-Bangalore-1" if region != "In-Bangalore-1" else "In-Hyderabad-2",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        if mode == "raw":
            response = client.highlvlvpc.with_raw_response.delete_instance(
                instanceKrn=instance_krn, deleteVolume=delete_volume, extra_headers={"x-test": "value"}, timeout=7
            )
            result = response.parse()
        elif mode == "streaming":
            with client.highlvlvpc.with_streaming_response.delete_instance(
                instanceKrn=instance_krn, deleteVolume=delete_volume, extra_headers={"x-test": "value"}, timeout=7
            ) as response:
                result = response.parse()
        else:
            result = client.highlvlvpc.delete_instance(
                instanceKrn=instance_krn, deleteVolume=delete_volume, extra_headers={"x-test": "value"}, timeout=7
            )
        assert result.message == "Deletion started"
        assert result.task_id == "task-id"


@pytest.mark.parametrize("region", SUPPORTED_REGIONS)
@pytest.mark.parametrize("delete_volume", [True, False])
@pytest.mark.parametrize("mode", ["parsed", "raw", "streaming"])
async def test_async_delete_instance_uses_krn_region(region: str, delete_volume: bool, mode: str) -> None:
    instance_krn = f"krn:vm:{region}:account:customer:instance:instance-id"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "DELETE"
        assert request.url.path == "/vm/v1/delete_instance_async"
        assert dict(request.url.params) == {"instanceKrn": instance_krn, "deleteVolume": str(delete_volume).lower()}
        assert request.headers["x-region"] == region
        assert request.headers["x-test"] == "value"
        assert request.extensions["timeout"]["read"] == 7
        return httpx.Response(202, json={"message": "Deletion started", "task_id": "task-id"})

    async with AsyncKrutrimClient(
        api_key="test-key",
        base_url="https://vm.test",
        region="In-Bangalore-1" if region != "In-Bangalore-1" else "In-Hyderabad-2",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        client._platform = "Linux"
        if mode == "raw":
            response = await client.highlvlvpc.with_raw_response.delete_instance(
                instanceKrn=instance_krn, deleteVolume=delete_volume, extra_headers={"x-test": "value"}, timeout=7
            )
            result = await response.parse()
        elif mode == "streaming":
            async with client.highlvlvpc.with_streaming_response.delete_instance(
                instanceKrn=instance_krn, deleteVolume=delete_volume, extra_headers={"x-test": "value"}, timeout=7
            ) as response:
                result = await response.parse()
        else:
            result = await client.highlvlvpc.delete_instance(
                instanceKrn=instance_krn, deleteVolume=delete_volume, extra_headers={"x-test": "value"}, timeout=7
            )
        assert result.message == "Deletion started"
        assert result.task_id == "task-id"
