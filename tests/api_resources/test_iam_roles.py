from __future__ import annotations

from typing import Any

import httpx
import pytest

from krutrim_client import KrutrimClient, AsyncKrutrimClient

FILTER_CASES = [
    ({}, "all"),
    ({"krutrimManaged": True}, "true"),
    ({"krutrimManaged": False}, "false"),
    ({"krutrimManaged": "all"}, "all"),
    ({"krutrimManaged": "TRUE"}, "true"),
    ({"krutrimManaged": "FALSE"}, "false"),
    ({"krutrim_managed": True}, "true"),
    ({"krutrim_managed": False}, "false"),
    ({"krutrim_managed": "all"}, "all"),
    ({"krutrimManaged": False, "krutrim_managed": True}, "false"),
]
ROLE_RESPONSE = {"roles": [], "totalCount": 0}


@pytest.mark.parametrize("filters,expected", FILTER_CASES)
@pytest.mark.parametrize("mode", ["parsed", "raw", "streaming"])
def test_list_roles_managed_filter(filters: dict[str, bool | str], expected: str, mode: str) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/iam/v1/roles"
        assert dict(request.url.params) == {"limit": "999", "offset": "0", "krutrimManaged": expected}
        assert request.headers["authorization"] == "Bearer test-key"
        assert request.headers["x-test"] == "value"
        return httpx.Response(200, json=ROLE_RESPONSE)

    with KrutrimClient(
        api_key="test-key",
        base_url="https://iam.test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        resource: Any = client.iam
        if mode == "raw":
            resource = resource.with_raw_response
        elif mode == "streaming":
            resource = resource.with_streaming_response
        result = resource.list_roles(limit=999, offset=0, extra_headers={"x-test": "value"}, **filters)
        if mode == "raw":
            result = result.parse()
        elif mode == "streaming":
            with result as response:
                result = response.parse()
        assert result == ROLE_RESPONSE


@pytest.mark.parametrize("filters,expected", FILTER_CASES)
@pytest.mark.parametrize("mode", ["parsed", "raw", "streaming"])
async def test_async_list_roles_managed_filter(filters: dict[str, bool | str], expected: str, mode: str) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/iam/v1/roles"
        assert dict(request.url.params) == {"limit": "999", "offset": "0", "krutrimManaged": expected}
        assert request.headers["authorization"] == "Bearer test-key"
        assert request.headers["x-test"] == "value"
        return httpx.Response(200, json=ROLE_RESPONSE)

    async with AsyncKrutrimClient(
        api_key="test-key",
        base_url="https://iam.test",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        client._platform = "Linux"
        resource: Any = client.iam
        if mode == "raw":
            resource = resource.with_raw_response
        elif mode == "streaming":
            resource = resource.with_streaming_response
        result = resource.list_roles(limit=999, offset=0, extra_headers={"x-test": "value"}, **filters)
        if mode == "streaming":
            async with result as response:
                result = await response.parse()
        else:
            result = await result
            if mode == "raw":
                result = await result.parse()
        assert result == ROLE_RESPONSE
