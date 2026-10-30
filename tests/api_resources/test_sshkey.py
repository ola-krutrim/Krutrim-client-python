from __future__ import annotations

import os

import httpx
import pytest
from respx import MockRouter

from krutrim_client import AsyncKrutrimClient, KrutrimClient
from krutrim_client.types.sshkey.sshkey_list_response import SshkeyListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

CUSTOMER_ID = "c97cdbd8-d903-4c15-8419-01e2278accc2"
X_REGION = "In-Bangalore-1"


@pytest.mark.respx(base_url=base_url)
def test_list_sshkeys_204_returns_empty_ssh_keys(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.get(f"/v2/sshkeys/{CUSTOMER_ID}").mock(return_value=httpx.Response(204))

    result = client.sshkey.list_sshkeys(
        customer_id=CUSTOMER_ID,
        x_region=X_REGION,
        page=1,
        limit=10,
    )

    assert route.called
    assert isinstance(result, SshkeyListResponse)
    assert result.ssh_keys == []
    assert route.calls.last.request.headers["k-customer-id"] == CUSTOMER_ID
    assert route.calls.last.request.headers["x-region"] == X_REGION


@pytest.mark.respx(base_url=base_url)
def test_list_sshkeys_empty_body_returns_empty_ssh_keys(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.get(f"/v2/sshkeys/{CUSTOMER_ID}").mock(
        return_value=httpx.Response(200, content=b"", headers={"content-type": "application/json"})
    )

    result = client.sshkey.list_sshkeys(
        customer_id=CUSTOMER_ID,
        x_region=X_REGION,
    )

    assert route.called
    assert result.ssh_keys == []


@pytest.mark.respx(base_url=base_url)
def test_list_sshkeys_with_meta_and_keys(client: KrutrimClient, respx_mock: MockRouter) -> None:
    payload = {
        "meta": {
            "limit": 10,
            "page": 1,
            "region": X_REGION,
            "sortBy": "createdAt",
            "sortOrder": "desc",
            "total": 1,
            "totalPages": 1,
        },
        "sshKeys": [
            {
                "_id": "krn:krutrim-ssh:In-Bangalore-1:acct:cust:sshkey:uuid-1",
                "accountId": "4144076351",
                "uuid": "uuid-1",
                "keyName": "my-key",
                "publicKey": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQ== test",
                "userId": CUSTOMER_ID,
                "createdBy": CUSTOMER_ID,
                "createdAt": "2026-10-20T05:32:08.303Z",
                "updatedAt": "2026-10-28T05:41:18.391Z",
                "vmAttached": [],
                "region": X_REGION,
                "status": "inactive",
                "expiresAt": "2027-01-18T05:32:08.303Z",
            }
        ],
    }
    route = respx_mock.get(f"/v2/sshkeys/{CUSTOMER_ID}").mock(return_value=httpx.Response(200, json=payload))

    result = client.sshkey.list_sshkeys(
        customer_id=CUSTOMER_ID,
        x_region=X_REGION,
        sort_by="createdAt",
        sort_order="desc",
        page=1,
        limit=10,
    )

    assert route.called
    assert result.meta is not None
    assert result.meta.total == 1
    assert result.meta.sort_by == "createdAt"
    assert len(result.ssh_keys) == 1
    assert result.ssh_keys[0].key_name == "my-key"
    assert result.ssh_keys[0].uuid == "uuid-1"
    assert "sortBy=createdAt" in str(route.calls.last.request.url)
    assert "sortOrder=desc" in str(route.calls.last.request.url)


@pytest.mark.respx(base_url=base_url)
@pytest.mark.asyncio
async def test_async_list_sshkeys_204_returns_empty_ssh_keys(
    async_client: AsyncKrutrimClient, respx_mock: MockRouter
) -> None:
    route = respx_mock.get(f"/v2/sshkeys/{CUSTOMER_ID}").mock(return_value=httpx.Response(204))

    result = await async_client.sshkey.list_sshkeys(
        customer_id=CUSTOMER_ID,
        x_region=X_REGION,
    )

    assert route.called
    assert result.ssh_keys == []
