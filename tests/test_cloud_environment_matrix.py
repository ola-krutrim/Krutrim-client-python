from __future__ import annotations

import json
import inspect
from typing import Any

import pytest
from respx import MockRouter

from krutrim_client import Environment, KrutrimClient, AsyncKrutrimClient, _client as client_module
from krutrim_client._models import FinalRequestOptions

CLIENT_TYPES = (KrutrimClient, AsyncKrutrimClient)
ENVIRONMENTS: tuple[tuple[Environment, str], ...] = (
    ("cloud", "https://cloud.olakrutrim.com"),
    ("cloudx", "https://cloudx.olakrutrim.com"),
)
REGION = "In-Hyderabad-1"


@pytest.fixture(autouse=True)
def isolate_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "KRUTRIMCLIENT_API_KEY",
        "KRUTRIM_API_KEY",
        "API_KEY",
        "KRUTRIMCLIENT_BASE_URL",
        "krutrim_client_BASE_URL",
        "KRUTRIM_CLIENT_BASE_URL",
        "KRUTRIM_BASE_URL",
        "BASE_URL",
        "KRUTRIM_ENVIRONMENT",
        "KRUTRIMCLIENT_ENVIRONMENT",
        "KRUTRIM_CLIENT_ENVIRONMENT",
        "ENVIRONMENT",
        "ENV",
        "KRUTRIM_REGION",
        "REGION",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(client_module, "_DOTENV_LOADED", True)


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
@pytest.mark.parametrize("environment,base_url", ENVIRONMENTS)
@pytest.mark.parametrize("login", ("root", "programmatic"))
async def test_login_and_authenticated_request_stay_in_selected_environment(
    client_type: type[Any], environment: Environment, base_url: str, login: str, respx_mock: MockRouter
) -> None:
    path = "/iam/v1/signInAsRootUser" if login == "root" else "/iam/v1/signinProgrammaticUser"
    token = f"{environment}-test-token"
    auth_route = respx_mock.post(base_url + path).respond(200, json={"access_token": token})
    users_route = respx_mock.get(base_url + "/iam/v1/users").respond(200, json={"users": []})
    client = client_type(environment=environment, region=REGION)
    try:
        if login == "root":
            result = client.iam.sign_in_as_root_user(email="test@example.com", password="test-password")
            expected_body = {"email": "test@example.com", "password": "test-password"}
        else:
            result = client.iam.signin_programmatic_user(account_id="account", access_key="access", secret_key="secret")
            expected_body = {"accountId": "account", "accessKey": "access", "secretKey": "secret"}
        if inspect.isawaitable(result):
            await result
        assert client.api_key == token
        assert client.token == token
        assert json.loads(auth_route.calls.last.request.content) == expected_body
        assert "authorization" not in auth_route.calls.last.request.headers

        result = client.iam.list_users(limit=10, offset=0)
        if inspect.isawaitable(result):
            await result
        request = users_route.calls.last.request
        assert request.headers["authorization"] == f"Bearer {token}"
        assert request.headers["x-region"] == REGION
        assert dict(request.url.params) == {"limit": "10", "offset": "0"}
    finally:
        if isinstance(client, AsyncKrutrimClient):
            await client.close()
        else:
            client.close()


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
@pytest.mark.parametrize("environment,base_url", ENVIRONMENTS)
@pytest.mark.parametrize(
    "resource,method,verb,path,arguments,query,body",
    (
        (
            "highlvlvpc",
            "search_vpcs",
            "GET",
            "/v2/highlvlvpc/search_vpc",
            {"x_region": REGION, "count": False, "order": "desc", "sort_by": "createdAt"},
            {"count": "false", "order": "desc", "sort_by": "createdAt"},
            None,
        ),
        (
            "kbs",
            "detach_volume",
            "POST",
            "/kbs/v1/volumes/volume-id/action",
            {
                "volume_id": "volume-id",
                "instance_id": "instance-id",
                "attachment_id": "attachment-id",
                "k_tenant_id": "tenant-id",
                "x_region": REGION,
            },
            {"op": "detach"},
            {"input": {"instanceId": "instance-id", "attachment_id": "attachment-id"}},
        ),
        (
            "sshkey",
            "create_sshkey",
            "POST",
            "/v2/sshkeys",
            {"key_name": "test-key", "public_key": "ssh-rsa test", "x_region": REGION, "customer_id": "customer-id"},
            {},
            {"keyName": "test-key", "publicKey": "ssh-rsa test"},
        ),
        (
            "securityGroup",
            "list_by_vpc",
            "GET",
            "/securityGroup/v1/vpc-id",
            {"vpc_id": "vpc-id", "x_region": REGION},
            {},
            None,
        ),
        (
            "sshkey",
            "delete_sshkey",
            "DELETE",
            "/v2/sshkeys/key-id",
            {"ssh_key_id": "key-id", "x_region": REGION, "customer_id": "customer-id"},
            {},
            None,
        ),
        (
            "lb",
            "list_load_balancers_by_vpc",
            "GET",
            "/api/v3/loadbalancer/getallbyvpc",
            {"vpc_krn": "vpc-id", "x_region": REGION, "page": 1, "limit": 10},
            {"vpc_krn": "vpc-id", "page": "1", "limit": "10"},
            None,
        ),
        (
            "startStopVM",
            "perform_action",
            "PUT",
            "/vm/v1/instance/instance-id",
            {"instance_krn": "instance-id", "x_region": REGION, "action": "stop"},
            {},
            {"action": "stop"},
        ),
    ),
)
async def test_migrated_resource_requests_on_both_environments(
    client_type: type[Any],
    environment: Environment,
    base_url: str,
    resource: str,
    method: str,
    verb: str,
    path: str,
    arguments: dict[str, Any],
    query: dict[str, str],
    body: Any,
    respx_mock: MockRouter,
) -> None:
    route = respx_mock.request(verb, base_url + path).respond(200, json={})
    client = client_type(api_key=f"{environment}-key", environment=environment)
    try:
        result = getattr(getattr(client, resource), method)(**arguments)
        if inspect.isawaitable(result):
            await result
        request = route.calls.last.request
        assert request.headers["authorization"] == f"Bearer {environment}-key"
        assert request.headers["x-region"] == REGION
        assert dict(request.url.params) == query
        if body is not None:
            assert json.loads(request.content) == body
        if resource == "kbs":
            assert request.headers["k-tenant-id"] == "tenant-id"
        if resource == "sshkey":
            assert request.headers["k-customer-id"] == "customer-id"
    finally:
        if isinstance(client, AsyncKrutrimClient):
            await client.close()
        else:
            client.close()


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_copy_changes_region_in_actual_request(client_type: type[Any]) -> None:
    client = client_type(api_key="test", environment="cloudx", region=REGION)
    copied = client.with_options(environment="cloud", region="In-Bangalore-1")
    request = copied._build_request(FinalRequestOptions(method="get", url="/iam/v1/users"))
    assert str(request.url) == "https://cloud.olakrutrim.com/iam/v1/users"
    assert request.headers["x-region"] == "In-Bangalore-1"
    assert client.default_headers["x-region"] == REGION
    assert client.region == REGION


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_copy_can_clear_key_before_signing_into_another_environment(client_type: type[Any]) -> None:
    client = client_type(api_key="cloudx-key", environment="cloudx")
    copied = client.copy(environment="cloud", api_key="")
    request = copied._build_request(FinalRequestOptions(method="post", url="/iam/v1/signInAsRootUser"))
    assert "authorization" not in request.headers
    assert client.api_key == "cloudx-key"


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
def test_region_header_is_case_insensitive(client_type: type[Any]) -> None:
    client = client_type(api_key="test", region=REGION, default_headers={"X-Region": "In-Bangalore-1"})
    request = client._build_request(FinalRequestOptions(method="get", url="/iam/v1/users"))
    assert request.headers.get_list("x-region") == ["In-Bangalore-1"]


@pytest.mark.parametrize("client_type", CLIENT_TYPES)
@pytest.mark.parametrize("variable", ("KRUTRIM_ENVIRONMENT", "KRUTRIMCLIENT_ENVIRONMENT", "KRUTRIM_CLIENT_ENVIRONMENT"))
def test_explicit_environment_overrides_environment_variables(
    client_type: type[Any], variable: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(variable, "cloudx")
    monkeypatch.setenv("KRUTRIMCLIENT_BASE_URL", "https://custom.example.com")
    client = client_type(api_key="test", environment="cloud")
    assert str(client.base_url) == "https://cloud.olakrutrim.com"
