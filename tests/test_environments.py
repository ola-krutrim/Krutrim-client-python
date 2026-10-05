from __future__ import annotations

from typing import Any
import httpx
import respx
import pytest

from krutrim_client import KrutrimClient, AsyncKrutrimClient, ENVIRONMENTS
from krutrim_client._models import FinalRequestOptions

API_KEY = "test-api-key"
CLIENT_TYPES = (KrutrimClient, AsyncKrutrimClient)
PROD_BASE_URL = "https://cloud.olakrutrim.com"
CLOUDX_BASE_URL = "https://cloudx.olakrutrim.com"

SEARCH_VPC_QUERY = {
    "count": "false",
    "order": "desc",
    "page": "1",
    "size": "10",
    "sort_by": "createdAt",
    "status": "active",
}


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_production_is_the_default_base_url(client_type: type[Any], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KRUTRIMCLIENT_BASE_URL", raising=False)
    monkeypatch.delenv("KRUTRIM_CLIENT_BASE_URL", raising=False)
    monkeypatch.delenv("krutrim_client_BASE_URL", raising=False)
    monkeypatch.delenv("KRUTRIM_ENVIRONMENT", raising=False)
    monkeypatch.delenv("KRUTRIMCLIENT_ENVIRONMENT", raising=False)

    client = client_type(api_key=API_KEY)
    assert client.base_url == PROD_BASE_URL


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_environment_cloudx_selection(client_type: type[Any], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KRUTRIMCLIENT_BASE_URL", raising=False)
    monkeypatch.delenv("KRUTRIM_CLIENT_BASE_URL", raising=False)
    monkeypatch.delenv("krutrim_client_BASE_URL", raising=False)

    client = client_type(api_key=API_KEY, environment="cloudx")
    assert client.base_url == CLOUDX_BASE_URL


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_environment_cloud_and_production_selection(client_type: type[Any], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KRUTRIMCLIENT_BASE_URL", raising=False)
    monkeypatch.delenv("KRUTRIM_CLIENT_BASE_URL", raising=False)
    monkeypatch.delenv("krutrim_client_BASE_URL", raising=False)

    client_prod = client_type(api_key=API_KEY, environment="production")
    assert client_prod.base_url == PROD_BASE_URL

    client_cloud = client_type(api_key=API_KEY, environment="cloud")
    assert client_cloud.base_url == PROD_BASE_URL


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_invalid_environment_raises(client_type: type[Any]) -> None:
    with pytest.raises(ValueError, match="Unknown environment"):
        client_type(api_key=API_KEY, environment="invalid_env")  # type: ignore[arg-type]


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_environment_variable_switches_to_cloudx(client_type: type[Any], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KRUTRIMCLIENT_BASE_URL", raising=False)
    monkeypatch.delenv("KRUTRIM_CLIENT_BASE_URL", raising=False)
    monkeypatch.delenv("krutrim_client_BASE_URL", raising=False)

    monkeypatch.setenv("KRUTRIM_ENVIRONMENT", "cloudx")
    client = client_type(api_key=API_KEY)
    assert client.base_url == CLOUDX_BASE_URL

    monkeypatch.delenv("KRUTRIM_ENVIRONMENT", raising=False)
    monkeypatch.setenv("KRUTRIMCLIENT_ENVIRONMENT", "cloudx")
    client2 = client_type(api_key=API_KEY)
    assert client2.base_url == CLOUDX_BASE_URL


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_base_url_env_overrides_default_environment(client_type: type[Any], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KRUTRIMCLIENT_BASE_URL", "https://custom.example.com")
    client = client_type(api_key=API_KEY)
    assert client.base_url == "https://custom.example.com"


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_both_base_url_and_environment_raises(client_type: type[Any]) -> None:
    with pytest.raises(ValueError, match="Both base_url and environment were given"):
        client_type(api_key=API_KEY, environment="cloudx", base_url="https://explicit.example.com")


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_explicit_base_url(client_type: type[Any], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KRUTRIMCLIENT_BASE_URL", "https://from-env.example.com")
    client = client_type(api_key=API_KEY, base_url="https://explicit.example.com")
    assert client.base_url == "https://explicit.example.com"


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_copy_preserves_environment_and_url(client_type: type[Any], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("KRUTRIMCLIENT_BASE_URL", raising=False)
    client = client_type(api_key=API_KEY, environment="cloudx")
    copied = client.copy()
    assert copied.base_url == CLOUDX_BASE_URL

    copied_prod = client.copy(environment="cloud")
    assert copied_prod.base_url == PROD_BASE_URL


def test_sync_vpc_search_with_cloudx_and_v2_endpoint() -> None:
    with respx.mock(assert_all_called=True) as router:
        route = router.get(f"{CLOUDX_BASE_URL}/v2/highlvlvpc/search_vpc", params=SEARCH_VPC_QUERY).mock(
            return_value=httpx.Response(200, json={})
        )
        client = KrutrimClient(api_key=API_KEY, environment="cloudx")
        client.highlvlvpc.search_vpcs(
            x_region="In-Bangalore-1",
            size=10,
            page=1,
            status="active",
            sort_by="createdAt",
            order="desc",
            count=False,
        )

    request = route.calls.last.request
    assert request.headers["x-region"] == "In-Bangalore-1"
    assert dict(request.url.params) == SEARCH_VPC_QUERY


@pytest.mark.asyncio
async def test_async_vpc_search_with_cloud_and_v2_endpoint() -> None:
    with respx.mock(assert_all_called=True) as router:
        route = router.get(f"{PROD_BASE_URL}/v2/highlvlvpc/search_vpc", params=SEARCH_VPC_QUERY).mock(
            return_value=httpx.Response(200, json={})
        )
        client = AsyncKrutrimClient(api_key=API_KEY, environment="cloud")
        await client.highlvlvpc.search_vpcs(
            x_region="In-Hyderabad-2",
            size=10,
            page=1,
            status="active",
            sort_by="createdAt",
            order="desc",
            count=False,
        )

    request = route.calls.last.request
    assert request.headers["x-region"] == "In-Hyderabad-2"
    assert dict(request.url.params) == SEARCH_VPC_QUERY
