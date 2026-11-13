from __future__ import annotations

from typing import Any

import httpx
import pytest

from krutrim_client import KrutrimClient, AsyncKrutrimClient
from krutrim_client.types.sandbox import SandboxResponse as ExistingSandboxResponse, SandboxGetResponse
from krutrim_client.types.sandbox_service import NetworkResponse, SandboxResponse


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("wrapper", ["parsed", "raw", "streaming"])
async def test_existing_and_new_components_share_client(asynchronous: bool, wrapper: str) -> None:
    """Keep existing routes and models intact across both sets of response wrappers."""
    paths: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        assert request.headers["authorization"] == "Bearer test-token"
        if request.url.path == "/omni/sandbox/v1/sandbox/existing-id":
            return httpx.Response(200, json={"status": 200, "data": {"id": "existing-id", "status": "active"}})
        assert request.url.path == "/sandbox/v1/sandboxes/krn-test/network"
        assert request.headers["x-region"] == "In-Bangalore-1"
        return httpx.Response(200, json={"code": "Network.Get", "details": {"egress": {"default_action": "deny"}}})

    client: Any = (
        AsyncKrutrimClient(
            api_key="test-token",
            base_url="https://cloud.olakrutrim.com",
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(handle)),
            _strict_response_validation=True,
        )
        if asynchronous
        else KrutrimClient(
            api_key="test-token",
            base_url="https://cloud.olakrutrim.com",
            http_client=httpx.Client(transport=httpx.MockTransport(handle)),
            _strict_response_validation=True,
        )
    )
    try:
        assert ExistingSandboxResponse is not SandboxResponse
        resource = client.sandbox
        if wrapper == "raw":
            resource = client.with_raw_response.sandbox
        elif wrapper == "streaming":
            resource = client.with_streaming_response.sandbox
        calls = [
            resource.api.retrieve("existing-id"),
            resource.network.retrieve(krn_id="krn-test", x_region="In-Bangalore-1"),
        ]
        results: list[Any] = []
        for call in calls:
            if wrapper == "streaming":
                if asynchronous:
                    async with call as response:
                        results.append(await response.parse())
                else:
                    with call as response:
                        results.append(response.parse())
            elif asynchronous:
                result = await call
                results.append(await result.parse() if wrapper == "raw" else result)
            else:
                results.append(call.parse() if wrapper == "raw" else call)
        existing, new = results
        assert isinstance(existing, SandboxGetResponse)
        assert isinstance(existing.data, ExistingSandboxResponse)
        assert existing.data.id == "existing-id"
        assert isinstance(new, NetworkResponse)
        assert new.details.egress is not None
        assert new.details.egress.default_action == "deny"
        assert len(paths) == 2
        assert callable(client.sandbox.create)
        assert callable(client.sandbox.connect)
    finally:
        if asynchronous:
            await client.close()
        else:
            client.close()
