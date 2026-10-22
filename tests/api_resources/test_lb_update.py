from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from krutrim_client import KrutrimClient, AsyncKrutrimClient
from krutrim_client.types.lb.update_load_balancer_params import UpdateLoadBalancerParams

REGION = "In-Hyderabad-2"
LB_KRN = f"krn:loadbalancer-service:{REGION}:account:customer:loadbalancer:lb-id"
LISTENER_KRN = f"krn:loadbalancer-service:{REGION}:account:customer:listener:listener-id"
POOL_KRN = f"krn:loadbalancer-service:{REGION}:account:customer:pool:pool-id"
TARGET_GROUP_KRN = f"krn:loadbalancer-service:{REGION}:account:customer:targetgroup:targetgroup-id"
POLICY_KRN = f"krn:loadbalancer-service:{REGION}:account:customer:policy:policy-id"
RULE_KRN = f"krn:loadbalancer-service:{REGION}:account:customer:rule:rule-id"

UPDATE_BODY: UpdateLoadBalancerParams = {
    "loadbalancer_krn": LB_KRN,
    "listener_krn": LISTENER_KRN,
    "listener": {"operation": "update", "name": "web"},
    "pool": [{"krn": POOL_KRN, "name": "poolx", "algorithm": "ROUND_ROBIN", "target_group_krn": TARGET_GROUP_KRN}],
    "policy": [
        {
            "operation": "update",
            "krn": POLICY_KRN,
            "name": "api",
            "action": "REDIRECT_TO_POOL",
            "redirect_pool_name": "poolx",
        }
    ],
    "rules": [
        {
            "operation": "update",
            "krn": RULE_KRN,
            "policy_krn": POLICY_KRN,
            "rule_type": "PATH",
            "compare_type": "EQUAL_TO",
            "value": "api",
        }
    ],
}
UPDATE_RESPONSE = {"code": "update.loadBalancer", "message": "loadbalancer updated successfully", "details": {}}


def update_handler(request: httpx.Request) -> httpx.Response:
    assert request.method == "PUT"
    assert request.url.host == "cloudx.olakrutrim.com"
    assert request.url.path == "/api/v3/loadbalancer"
    assert request.headers["x-region"] == REGION
    assert request.headers["k-customer-id"] == "customer"
    assert request.headers["x-account-id"] == "account"
    assert request.headers["content-type"] == "application/json"
    assert request.headers["x-test"] == "value"
    assert request.url.params["request"] == "test"
    assert request.extensions["timeout"]["read"] == 7
    assert json.loads(request.content) == UPDATE_BODY
    return httpx.Response(200, json=UPDATE_RESPONSE)


@pytest.mark.parametrize("mode", ["parsed", "raw", "streaming"])
def test_update_load_balancer_matches_cloudx_api(mode: str) -> None:
    with KrutrimClient(
        api_key="test-key",
        environment="cloudx",
        http_client=httpx.Client(transport=httpx.MockTransport(update_handler)),
        max_retries=0,
    ) as client:
        resource: Any = client.lb
        if mode == "raw":
            resource = resource.with_raw_response
        elif mode == "streaming":
            resource = resource.with_streaming_response
        result = resource.update_load_balancer(
            LB_KRN,
            x_region=REGION,
            k_customer_id="customer",
            x_account_id="account",
            listener_krn=LISTENER_KRN,
            listener=UPDATE_BODY["listener"],
            pool=UPDATE_BODY["pool"],
            policy=UPDATE_BODY["policy"],
            rules=UPDATE_BODY["rules"],
            extra_headers={"x-test": "value"},
            extra_query={"request": "test"},
            timeout=7,
        )
        if mode == "raw":
            result = result.parse()
        elif mode == "streaming":
            with result as response:
                result = response.parse()
        assert result == UPDATE_RESPONSE


def test_update_load_balancer_can_update_description_only() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v3/loadbalancer"
        assert json.loads(request.content) == {"loadbalancer_krn": LB_KRN, "loadbalancer": {"description": ""}}
        return httpx.Response(200, json=UPDATE_RESPONSE)

    with KrutrimClient(
        api_key="test-key",
        environment="cloudx",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        assert (
            client.lb.update_load_balancer(LB_KRN, x_region=REGION, loadbalancer={"description": ""}) == UPDATE_RESPONSE
        )


async def test_async_update_load_balancer_can_update_description_only() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v3/loadbalancer"
        assert json.loads(request.content) == {"loadbalancer_krn": LB_KRN, "loadbalancer": {"description": ""}}
        return httpx.Response(200, json=UPDATE_RESPONSE)

    async with AsyncKrutrimClient(
        api_key="test-key",
        environment="cloudx",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        max_retries=0,
    ) as client:
        client._platform = "Linux"
        assert (
            await client.lb.update_load_balancer(LB_KRN, x_region=REGION, loadbalancer={"description": ""})
            == UPDATE_RESPONSE
        )


@pytest.mark.parametrize("mode", ["parsed", "raw", "streaming"])
async def test_async_update_load_balancer_matches_cloudx_api(mode: str) -> None:
    async with AsyncKrutrimClient(
        api_key="test-key",
        environment="cloudx",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(update_handler)),
        max_retries=0,
    ) as client:
        client._platform = "Linux"
        resource: Any = client.lb
        if mode == "raw":
            resource = resource.with_raw_response
        elif mode == "streaming":
            resource = resource.with_streaming_response
        result = resource.update_load_balancer(
            LB_KRN,
            x_region=REGION,
            k_customer_id="customer",
            x_account_id="account",
            listener_krn=LISTENER_KRN,
            listener=UPDATE_BODY["listener"],
            pool=UPDATE_BODY["pool"],
            policy=UPDATE_BODY["policy"],
            rules=UPDATE_BODY["rules"],
            extra_headers={"x-test": "value"},
            extra_query={"request": "test"},
            timeout=7,
        )
        if mode == "streaming":
            async with result as response:
                result = await response.parse()
        else:
            result = await result
            if mode == "raw":
                result = await result.parse()
        assert result == UPDATE_RESPONSE
