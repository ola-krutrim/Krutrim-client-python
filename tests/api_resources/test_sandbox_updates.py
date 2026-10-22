from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from krutrim_client import KrutrimClient, AsyncKrutrimClient

SANDBOX_ID = "d4231c8b-28b9-428c-a228-597dbcc4f015"
BASE_URL = "https://r1.staging.olakrutrim.com"
UPDATE_CASES = [
    ("set_flavor", "flavor", "sandbox-large-hyd", {"flavorName": "sandbox-large-hyd"}),
    ("set_ttl", "ttl", 20000, {"ttlSeconds": 20000}),
]


@pytest.mark.parametrize("method,endpoint,value,body", UPDATE_CASES)
@pytest.mark.parametrize("mode", ["parsed", "raw", "streaming"])
def test_sandbox_updates_use_put(
    method: str, endpoint: str, value: str | int, body: dict[str, object], mode: str
) -> None:
    response_body = {"status": 200, "data": {"id": SANDBOX_ID, **body}}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PUT"
        assert request.url.path == f"/omni/sandbox/v1/sandbox/{SANDBOX_ID}/{endpoint}"
        assert json.loads(request.content) == body
        assert request.headers["x-account-id"] == "account-id"
        assert request.headers["x-user-email"] == "test@example.com"
        assert request.url.params["request"] == "test"
        assert request.extensions["timeout"]["read"] == 7
        return httpx.Response(200, json=response_body)

    with KrutrimClient(
        api_key="test-key",
        base_url=BASE_URL,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        api: Any = client.sandbox.api
        if mode == "raw":
            api = client.with_raw_response.sandbox.api
        elif mode == "streaming":
            api = client.with_streaming_response.sandbox.api
        result = getattr(api, method)(
            SANDBOX_ID,
            value,
            extra_headers={"x-account-id": "account-id", "x-user-email": "test@example.com"},
            extra_query={"request": "test"},
            timeout=7,
        )
        if mode == "raw":
            assert result.json() == response_body
        elif mode == "streaming":
            with result as response:
                assert response.json() == response_body
        elif method == "set_ttl":
            assert result.data.ttl_seconds == 20000
        else:
            assert result == response_body


@pytest.mark.parametrize("method,endpoint,value,body", UPDATE_CASES)
@pytest.mark.parametrize("mode", ["parsed", "raw", "streaming"])
async def test_async_sandbox_updates_use_put(
    method: str, endpoint: str, value: str | int, body: dict[str, object], mode: str
) -> None:
    response_body = {"status": 200, "data": {"id": SANDBOX_ID, **body}}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PUT"
        assert request.url.path == f"/omni/sandbox/v1/sandbox/{SANDBOX_ID}/{endpoint}"
        assert json.loads(request.content) == body
        assert request.headers["x-account-id"] == "account-id"
        assert request.headers["x-user-email"] == "test@example.com"
        assert request.url.params["request"] == "test"
        assert request.extensions["timeout"]["read"] == 7
        return httpx.Response(200, json=response_body)

    async with AsyncKrutrimClient(
        api_key="test-key",
        base_url=BASE_URL,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        client._platform = "Linux"
        api: Any = client.sandbox.api
        if mode == "raw":
            api = client.with_raw_response.sandbox.api
        elif mode == "streaming":
            api = client.with_streaming_response.sandbox.api
        result = getattr(api, method)(
            SANDBOX_ID,
            value,
            extra_headers={"x-account-id": "account-id", "x-user-email": "test@example.com"},
            extra_query={"request": "test"},
            timeout=7,
        )
        if mode == "streaming":
            async with result as response:
                assert await response.json() == response_body
        else:
            result = await result
            if mode == "raw":
                assert await result.json() == response_body
            elif method == "set_ttl":
                assert result.data.ttl_seconds == 20000
            else:
                assert result == response_body


@pytest.mark.parametrize("sandbox_id,flavor_name", [("", "sandbox-large-hyd"), (SANDBOX_ID, ""), (SANDBOX_ID, " ")])
async def test_set_flavor_rejects_empty_parameters(sandbox_id: str, flavor_name: str) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        pytest.fail(f"Unexpected request: {request.url}")

    with KrutrimClient(
        api_key="test-key",
        base_url=BASE_URL,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        with pytest.raises(ValueError):
            client.sandbox.api.set_flavor(sandbox_id, flavor_name)
    async with AsyncKrutrimClient(
        api_key="test-key",
        base_url=BASE_URL,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        with pytest.raises(ValueError):
            await client.sandbox.api.set_flavor(sandbox_id, flavor_name)


def test_bound_set_timeout_uses_put() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            return httpx.Response(200, json={"status": 200, "data": {"id": SANDBOX_ID, "status": "active"}})
        assert request.method == "PUT"
        assert request.url.path == f"/omni/sandbox/v1/sandbox/{SANDBOX_ID}/ttl"
        assert json.loads(request.content) == {"ttlSeconds": 20000}
        return httpx.Response(200, json={"status": 200, "data": {"id": SANDBOX_ID, "ttlSeconds": 20000}})

    with KrutrimClient(
        api_key="test-key",
        base_url=BASE_URL,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        sandbox = client.sandbox.connect(SANDBOX_ID)
        sandbox.set_timeout(20000)
        assert sandbox.metadata.ttl_seconds == 20000


async def test_async_bound_set_timeout_uses_put() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            return httpx.Response(200, json={"status": 200, "data": {"id": SANDBOX_ID, "status": "active"}})
        assert request.method == "PUT"
        assert request.url.path == f"/omni/sandbox/v1/sandbox/{SANDBOX_ID}/ttl"
        assert json.loads(request.content) == {"ttlSeconds": 20000}
        return httpx.Response(200, json={"status": 200, "data": {"id": SANDBOX_ID, "ttlSeconds": 20000}})

    async with AsyncKrutrimClient(
        api_key="test-key",
        base_url=BASE_URL,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        client._platform = "Linux"
        sandbox = await client.sandbox.connect(SANDBOX_ID)
        await sandbox.set_timeout(20000)
        assert sandbox.metadata.ttl_seconds == 20000
