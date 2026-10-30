from __future__ import annotations

import os

import httpx
import pytest
from respx import MockRouter

from krutrim_client import AsyncKrutrimClient, KrutrimClient

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

CUSTOMER_ID = "customer-id"
X_REGION = "In-Hyderabad-1"


@pytest.mark.respx(base_url=base_url)
def test_list_sshkeys_204_returns_empty_list(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.get(f"/v2/sshkeys/{CUSTOMER_ID}").mock(return_value=httpx.Response(204))

    result = client.sshkey.list_sshkeys(
        customer_id=CUSTOMER_ID,
        x_region=X_REGION,
        page=1,
        limit=10,
    )

    assert route.called
    assert result == []


@pytest.mark.respx(base_url=base_url)
def test_list_sshkeys_empty_body_returns_empty_list(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.get(f"/v2/sshkeys/{CUSTOMER_ID}").mock(
        return_value=httpx.Response(200, content=b"", headers={"content-type": "application/json"})
    )

    result = client.sshkey.list_sshkeys(
        customer_id=CUSTOMER_ID,
        x_region=X_REGION,
    )

    assert route.called
    assert result == []


@pytest.mark.respx(base_url=base_url)
def test_list_sshkeys_with_keys(client: KrutrimClient, respx_mock: MockRouter) -> None:
    payload = [{"keyName": "my-key", "id": "key-1"}]
    route = respx_mock.get(f"/v2/sshkeys/{CUSTOMER_ID}").mock(
        return_value=httpx.Response(200, json=payload)
    )

    result = client.sshkey.list_sshkeys(
        customer_id=CUSTOMER_ID,
        x_region=X_REGION,
    )

    assert route.called
    assert result == payload


@pytest.mark.respx(base_url=base_url)
@pytest.mark.asyncio
async def test_async_list_sshkeys_204_returns_empty_list(
    async_client: AsyncKrutrimClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.get(f"/v2/sshkeys/{CUSTOMER_ID}").mock(return_value=httpx.Response(204))

    result = await async_client.sshkey.list_sshkeys(
        customer_id=CUSTOMER_ID,
        x_region=X_REGION,
    )

    assert route.called
    assert result == []
