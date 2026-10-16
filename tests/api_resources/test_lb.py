from __future__ import annotations

import os
import json
from urllib.parse import quote

import httpx
import pytest
from respx import MockRouter

from krutrim_client import KrutrimClient, AsyncKrutrimClient
from krutrim_client.types.lb.create_target_group_params import CreateTargetGroupParams
from krutrim_client.types.lb.update_target_group_params import (
    Member as TargetGroupUpdateMember,
    HealthMonitor as TargetGroupUpdateHealthMonitor,
)
from krutrim_client.types.lb.create_load_balancer_params import LoadBalancerData
from krutrim_client.types.lb.update_load_balancer_params import (
    PoolUpdate,
    RuleOperation,
    ListenerUpdate,
    PolicyOperation,
    LoadBalancerUpdate,
    UpdateLoadBalancerParams,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

K_CUSTOMER_ID = "customer-id"
X_ACCOUNT_ID = "account-id"
X_REGION = "In-Bangalore-1"
VPC_KRN = "krn:vpc:In-Bangalore-1:account-id:customer-id:vpc:vpc-id"
LB_KRN = "krn:loadbalancer-service:In-Bangalore-1:account-id:customer-id:loadbalancer:lb-id"
LISTENER_KRN = "krn:loadbalancer-service:In-Bangalore-1:account-id:customer-id:listener:listener-id"
POLICY_KRN = "krn:loadbalancer-service:In-Bangalore-1:account-id:customer-id:policy:policy-id"
RULE_KRN = "krn:loadbalancer-service:In-Bangalore-1:account-id:customer-id:rule:rule-id"
POOL_KRN = "krn:loadbalancer-service:In-Bangalore-1:account-id:customer-id:pool:pool-id"
TARGET_GROUP_KRN = "krn:loadbalancer-service:In-Bangalore-1:account-id:customer-id:targetgroup:target-group-id"

TARGET_GROUP_BODY: CreateTargetGroupParams = {
    "target_group_name": "example-target-group",
    "vpc_krn": VPC_KRN,
    "lb_krn": [],
    "members": [{"name": "member-1", "address": "192.168.1.155", "protocol_port": 700, "weight": 1}],
    "health_monitor": {
        "delay": 10,
        "timeout": 5,
        "max_retries": 3,
        "health_check_path": "/",
        "type": "HTTP",
        "name": "health-monitor-1",
    },
}

LOAD_BALANCER_DATA: LoadBalancerData = {
    "name": "example-load-balancer",
    "description": "",
    "floating_ip": True,
    "vpc_id": VPC_KRN,
    "network_id": "network-krn",
    "vip_subnet_id": "subnet-krn",
    "type": "ALB",
    "flavor": "standard",
    "security_group_krns": ["security-group-krn"],
    "listeners": [
        {
            "name": "http-listener",
            "protocol": "HTTP",
            "protocol_port": 80,
            "default_pool": True,
            "pool_data": [
                {
                    "name": "default-pool",
                    "description": "",
                    "algorithm": "ROUND_ROBIN",
                    "protocol": "HTTP",
                    "target_group_name": "example-target-group",
                }
            ],
            "l7_policies": [
                {
                    "policy_name": "example-policy",
                    "action": "REDIRECT_TO_URL",
                    "position": 1,
                    "redirect_url": "https://example.com",
                    "rules": [{"type": "PATH", "compare_type": "EQUAL_TO", "value": "/health"}],
                }
            ],
        }
    ],
}

NETWORK_LOAD_BALANCER_DATA: LoadBalancerData = {
    "name": "example-network-load-balancer",
    "description": "",
    "floating_ip": False,
    "vpc_id": VPC_KRN,
    "network_id": "network-krn",
    "vip_subnet_id": "subnet-krn",
    "type": "NLB",
    "flavor": "standard",
    "security_group_krns": ["security-group-krn"],
    "listeners": [
        {
            "name": "tcp-listener",
            "protocol": "TCP",
            "protocol_port": 80,
            "default_pool": True,
            "pool_data": [
                {
                    "name": "tcp-pool",
                    "description": "",
                    "algorithm": "ROUND_ROBIN",
                    "protocol": "TCP",
                    "target_group_name": "example-target-group",
                }
            ],
            "l7_policies": [],
        }
    ],
}

LISTENER_UPDATE: ListenerUpdate = {
    "operation": "update",
    "name": "listener-updated",
    "sni_container_refs": ["cert", "cert-2"],
}

LOAD_BALANCER_UPDATE: LoadBalancerUpdate = {
    "description": "Updated load balancer for production traffic",
    "security_group_krn": ["security-group-krn"],
}

POLICY_OPERATIONS: list[PolicyOperation] = [
    {
        "operation": "update",
        "krn": POLICY_KRN,
        "name": "http-header-policy",
        "action": "REDIRECT_TO_POOL",
        "description": "Updated policy description",
        "redirect_pool_name": "backend-pool-v2",
    },
    {
        "operation": "create",
        "name": "new-redirect-policy",
        "action": "REDIRECT_TO_URL",
        "description": "New policy for URL redirection",
        "redirect_url": "https://example.com/new-path",
        "redirect_http_code": 302,
        "position": 2,
        "admin_state_up": True,
        "tags": ["new", "redirect"],
    },
    {
        "operation": "delete",
        "krn": "policy-to-delete-krn",
    },
]

RULE_OPERATIONS: list[RuleOperation] = [
    {
        "operation": "create",
        "policy_krn": POLICY_KRN,
        "rule_type": "HEADER",
        "compare_type": "EQUAL_TO",
        "key": "x-forwarded-for",
        "value": "true",
    },
    {
        "operation": "update",
        "krn": RULE_KRN,
        "policy_krn": POLICY_KRN,
        "rule_type": "HEADER",
        "compare_type": "CONTAINS",
        "key": "user-agent",
        "value": "Mozilla",
    },
]

POOL_UPDATES: list[PoolUpdate] = [
    {
        "krn": POOL_KRN,
        "name": "backend-pool-v2",
        "algorithm": "SOURCE_IP",
        "target_group_krn": TARGET_GROUP_KRN,
    }
]

UPDATE_LOAD_BALANCER_BODY: UpdateLoadBalancerParams = {
    "loadbalancer_krn": LB_KRN,
    "listener_krn": LISTENER_KRN,
    "listener": LISTENER_UPDATE,
    "loadbalancer": LOAD_BALANCER_UPDATE,
    "policy": POLICY_OPERATIONS,
    "rules": RULE_OPERATIONS,
    "pool": POOL_UPDATES,
}

TARGET_GROUP_UPDATE_MEMBERS: list[TargetGroupUpdateMember] = [
    {
        "name": "member-updated",
        "weight": 1,
        "address": "192.168.1.155",
        "protocol_port": 700,
    }
]

TARGET_GROUP_UPDATE_HEALTH_MONITOR: TargetGroupUpdateHealthMonitor = {
    "delay": 10,
    "timeout": 5,
    "max_retries": 2,
    "health_check_path": "/",
    "name": "health-monitor-updated",
}

UPDATE_TARGET_GROUP_BODY = {
    "krn": TARGET_GROUP_KRN,
    "members": TARGET_GROUP_UPDATE_MEMBERS,
    "health_monitor": TARGET_GROUP_UPDATE_HEALTH_MONITOR,
}

CREATE_TARGET_GROUP_RESPONSE = {
    "code": "create.targetGroup",
    "message": "target group created successfully",
    "details": {
        "target_group_krn": "target-group-krn",
        "req_id": "request-id",
        "name": "example-target-group",
        "k_customer_id": K_CUSTOMER_ID,
        "x_account_id": X_ACCOUNT_ID,
        "region": X_REGION,
        "loadbalancer_krn": [],
        "vpc_krn": VPC_KRN,
        "health_monitor": "health-monitor-1",
        "members": ["member-1"],
    },
}

LIST_TARGET_GROUPS_RESPONSE = {
    "code": "get.allTargetGroups",
    "message": "target groups fetched successfully",
    "details": [
        {
            "name": "example-target-group",
            "target_group_krn": "target-group-krn",
            "target_type": "instance",
            "load_balancers": [],
            "members": [
                {
                    "name": "member-1",
                    "address": "192.168.1.155",
                    "port": 700,
                    "weight": 1,
                    "operating_status": "ONLINE",
                    "type": "VM",
                }
            ],
            "health_check": {
                "name": "health-monitor-1",
                "protocol": "HTTP",
                "path": "/",
                "delay": 10,
                "timeout": 5,
                "max_retries": 3,
            },
            "vpc_krn": VPC_KRN,
            "created_at": "2026-08-24T10:53:36Z",
        }
    ],
}

CREATE_LOAD_BALANCER_RESPONSE = {
    "code": "create.loadBalancer",
    "message": "loadbalancer creation request accepted",
    "details": "task-id",
}

UPDATE_TARGET_GROUP_RESPONSE = {
    "code": "update.targetGroup",
    "message": "target group update request accepted",
    "details": {
        "loadbalancer_krn": [],
        "members": ["member-updated"],
        "req_id": "request-id",
        "target_group_krn": TARGET_GROUP_KRN,
        "target_group_name": "example-target-group",
        "vpc_krn": VPC_KRN,
    },
}

DELETE_TARGET_GROUP_RESPONSE = {
    "code": "delete.targetGroup",
    "message": "target group deleted successfully",
}

LIST_LOAD_BALANCERS_RESPONSE = {
    "code": "LoadBalancer.Get",
    "message": "Load balancers fetched successfully",
    "details": {
        "loadbalancers": [
            {
                "lb_krn": "load-balancer-krn",
                "lb_name": "example-load-balancer",
                "lb_type": "ALB",
                "flavor": "standard",
                "provisioning_status": "PENDING_CREATE",
                "operating_status": "OFFLINE",
                "status": "creating",
                "vip_address": "192.168.1.246",
                "floating_ip": "10.230.159.74",
                "created_on": 1787569150,
            }
        ],
        "pagination": {
            "current_page": 1,
            "total_pages": 1,
            "total_count": 1,
            "page": 1,
            "limit": 10,
            "offset": 0,
        },
    },
}


def _assert_request_headers(request: httpx.Request) -> None:
    assert request.headers["authorization"] == "Bearer My API Key"
    assert request.headers["k-customer-id"] == K_CUSTOMER_ID
    assert request.headers["x-account-id"] == X_ACCOUNT_ID
    assert request.headers["x-region"] == X_REGION


@pytest.mark.respx(base_url=base_url)
def test_create_target_group(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.post("/api/v3/loadBalancer/targetgroup").mock(
        return_value=httpx.Response(200, json=CREATE_TARGET_GROUP_RESPONSE)
    )

    response = client.lb.create_target_group(
        target_group_name=TARGET_GROUP_BODY["target_group_name"],
        vpc_krn=TARGET_GROUP_BODY["vpc_krn"],
        lb_krn=TARGET_GROUP_BODY["lb_krn"],
        members=TARGET_GROUP_BODY["members"],
        health_monitor=TARGET_GROUP_BODY["health_monitor"],
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )

    assert response.details.target_group_krn == "target-group-krn"
    request = route.calls.last.request
    _assert_request_headers(request)
    assert json.loads(request.content) == TARGET_GROUP_BODY


@pytest.mark.respx(base_url=base_url)
def test_list_target_groups(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.get("/api/v3/loadBalancer/targetgroups").mock(
        return_value=httpx.Response(200, json=LIST_TARGET_GROUPS_RESPONSE)
    )

    response = client.lb.list_target_groups(
        vpc_krn=VPC_KRN,
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )

    assert response.details[0].members[0].port == 700
    request = route.calls.last.request
    _assert_request_headers(request)
    assert dict(request.url.params) == {"vpc_krn": VPC_KRN}


@pytest.mark.respx(base_url=base_url)
def test_update_target_group(client: KrutrimClient, respx_mock: MockRouter) -> None:
    encoded_krn = quote(TARGET_GROUP_KRN, safe="")
    route = respx_mock.put(f"/api/v3/loadBalancer/targetgroup/{encoded_krn}").mock(
        return_value=httpx.Response(202, json=UPDATE_TARGET_GROUP_RESPONSE)
    )

    response = client.lb.update_target_group(
        TARGET_GROUP_KRN,
        members=TARGET_GROUP_UPDATE_MEMBERS,
        health_monitor=TARGET_GROUP_UPDATE_HEALTH_MONITOR,
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )

    assert response.details.target_group_krn == TARGET_GROUP_KRN
    request = route.calls.last.request
    _assert_request_headers(request)
    assert request.url.raw_path == f"/api/v3/loadBalancer/targetgroup/{encoded_krn}".encode()
    assert json.loads(request.content) == UPDATE_TARGET_GROUP_BODY


@pytest.mark.respx(base_url=base_url)
def test_delete_target_group(client: KrutrimClient, respx_mock: MockRouter) -> None:
    encoded_krn = quote(TARGET_GROUP_KRN, safe="")
    route = respx_mock.delete(f"/api/v3/loadBalancer/targetgroup/{encoded_krn}").mock(
        return_value=httpx.Response(200, json=DELETE_TARGET_GROUP_RESPONSE)
    )

    response = client.lb.delete_target_group(
        TARGET_GROUP_KRN,
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )

    assert response.code == "delete.targetGroup"
    request = route.calls.last.request
    _assert_request_headers(request)
    assert request.url.raw_path == f"/api/v3/loadBalancer/targetgroup/{encoded_krn}".encode()


@pytest.mark.respx(base_url=base_url)
def test_create_load_balancer(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.post("/api/v3/loadbalancer").mock(
        return_value=httpx.Response(202, json=CREATE_LOAD_BALANCER_RESPONSE)
    )

    response = client.lb.create_load_balancer(
        loadbalancer_data=LOAD_BALANCER_DATA,
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )

    assert response.details == "task-id"
    request = route.calls.last.request
    _assert_request_headers(request)
    assert json.loads(request.content) == {"loadbalancer_data": LOAD_BALANCER_DATA}


@pytest.mark.respx(base_url=base_url)
def test_create_network_load_balancer(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.post("/api/v3/loadbalancer").mock(
        return_value=httpx.Response(
            202,
            json={
                **CREATE_LOAD_BALANCER_RESPONSE,
                "details": "network-load-balancer-task-id",
            },
        )
    )

    response = client.lb.create_load_balancer(
        loadbalancer_data=NETWORK_LOAD_BALANCER_DATA,
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )

    assert response.details == "network-load-balancer-task-id"
    request = route.calls.last.request
    _assert_request_headers(request)
    assert json.loads(request.content) == {"loadbalancer_data": NETWORK_LOAD_BALANCER_DATA}


@pytest.mark.respx(base_url=base_url)
def test_list_load_balancers_by_vpc(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.get("/api/v3/loadbalancer/getallbyvpc").mock(
        return_value=httpx.Response(200, json=LIST_LOAD_BALANCERS_RESPONSE)
    )

    response = client.lb.list_load_balancers_by_vpc(
        vpc_krn=VPC_KRN,
        page=1,
        limit=10,
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )

    assert response.details.loadbalancers[0].floating_ip == "10.230.159.74"
    request = route.calls.last.request
    _assert_request_headers(request)
    assert dict(request.url.params) == {"vpc_krn": VPC_KRN, "page": "1", "limit": "10"}


@pytest.mark.respx(base_url=base_url)
def test_list_load_balancers_by_vpc_with_region_only(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.get("/api/v3/loadbalancer/getallbyvpc").mock(
        return_value=httpx.Response(200, json=LIST_LOAD_BALANCERS_RESPONSE)
    )

    client.lb.list_load_balancers_by_vpc(vpc_krn=VPC_KRN, x_region=X_REGION)

    request = route.calls.last.request
    assert request.headers["x-region"] == X_REGION
    assert "k-customer-id" not in request.headers
    assert "x-account-id" not in request.headers
    assert dict(request.url.params) == {"vpc_krn": VPC_KRN}


@pytest.mark.respx(base_url=base_url)
def test_update_load_balancer(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.put(f"/api/v3/loadbalancer/{LB_KRN}").mock(
        return_value=httpx.Response(
            200,
            json={"code": "update.loadBalancer", "message": "loadbalancer updated successfully", "details": {}},
        )
    )

    client.lb.update_load_balancer(
        LB_KRN,
        x_region=X_REGION,
        listener_krn=LISTENER_KRN,
        listener=LISTENER_UPDATE,
        loadbalancer=LOAD_BALANCER_UPDATE,
        policy=POLICY_OPERATIONS,
        rules=RULE_OPERATIONS,
        pool=POOL_UPDATES,
    )

    request = route.calls.last.request
    assert request.headers["x-region"] == X_REGION
    assert json.loads(request.content) == UPDATE_LOAD_BALANCER_BODY


@pytest.mark.respx(base_url=base_url)
def test_delete_load_balancer(client: KrutrimClient, respx_mock: MockRouter) -> None:
    route = respx_mock.delete(f"/api/v3/loadbalancer/{LB_KRN}").mock(return_value=httpx.Response(204))

    response = client.lb.delete_load_balancer(LB_KRN, x_region=X_REGION)

    assert response is None
    request = route.calls.last.request
    assert request.headers["x-region"] == X_REGION
    assert "k-customer-id" not in request.headers
    assert "x-account-id" not in request.headers


@pytest.mark.respx(base_url=base_url)
async def test_async_load_balancer_endpoints(async_client: AsyncKrutrimClient, respx_mock: MockRouter) -> None:
    create_target_group = respx_mock.post("/api/v3/loadBalancer/targetgroup").mock(
        return_value=httpx.Response(200, json=CREATE_TARGET_GROUP_RESPONSE)
    )
    list_target_groups = respx_mock.get("/api/v3/loadBalancer/targetgroups").mock(
        return_value=httpx.Response(200, json=LIST_TARGET_GROUPS_RESPONSE)
    )
    encoded_target_group_krn = quote(TARGET_GROUP_KRN, safe="")
    update_target_group = respx_mock.put(f"/api/v3/loadBalancer/targetgroup/{encoded_target_group_krn}").mock(
        return_value=httpx.Response(202, json=UPDATE_TARGET_GROUP_RESPONSE)
    )
    delete_target_group = respx_mock.delete(f"/api/v3/loadBalancer/targetgroup/{encoded_target_group_krn}").mock(
        return_value=httpx.Response(200, json=DELETE_TARGET_GROUP_RESPONSE)
    )
    create_load_balancer = respx_mock.post("/api/v3/loadbalancer").mock(
        return_value=httpx.Response(202, json=CREATE_LOAD_BALANCER_RESPONSE)
    )
    list_load_balancers = respx_mock.get("/api/v3/loadbalancer/getallbyvpc").mock(
        return_value=httpx.Response(200, json=LIST_LOAD_BALANCERS_RESPONSE)
    )
    update_load_balancer = respx_mock.put(f"/api/v3/loadbalancer/{LB_KRN}").mock(
        return_value=httpx.Response(200, json={"message": "updated"})
    )
    delete_load_balancer = respx_mock.delete(f"/api/v3/loadbalancer/{LB_KRN}").mock(return_value=httpx.Response(204))

    await async_client.lb.create_target_group(
        target_group_name=TARGET_GROUP_BODY["target_group_name"],
        vpc_krn=TARGET_GROUP_BODY["vpc_krn"],
        lb_krn=TARGET_GROUP_BODY["lb_krn"],
        members=TARGET_GROUP_BODY["members"],
        health_monitor=TARGET_GROUP_BODY["health_monitor"],
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )
    await async_client.lb.list_target_groups(
        vpc_krn=VPC_KRN,
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )
    await async_client.lb.update_target_group(
        TARGET_GROUP_KRN,
        members=TARGET_GROUP_UPDATE_MEMBERS,
        health_monitor=TARGET_GROUP_UPDATE_HEALTH_MONITOR,
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )
    await async_client.lb.delete_target_group(
        TARGET_GROUP_KRN,
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )
    await async_client.lb.create_load_balancer(
        loadbalancer_data=LOAD_BALANCER_DATA,
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )
    await async_client.lb.list_load_balancers_by_vpc(
        vpc_krn=VPC_KRN,
        k_customer_id=K_CUSTOMER_ID,
        x_account_id=X_ACCOUNT_ID,
        x_region=X_REGION,
    )
    await async_client.lb.update_load_balancer(
        LB_KRN,
        x_region=X_REGION,
        listener_krn=LISTENER_KRN,
        listener=LISTENER_UPDATE,
        loadbalancer=LOAD_BALANCER_UPDATE,
        policy=POLICY_OPERATIONS,
        rules=RULE_OPERATIONS,
        pool=POOL_UPDATES,
    )
    await async_client.lb.delete_load_balancer(LB_KRN, x_region=X_REGION)

    assert create_target_group.called
    assert list_target_groups.called
    assert update_target_group.called
    assert delete_target_group.called
    assert create_load_balancer.called
    assert list_load_balancers.called
    assert update_load_balancer.called
    assert delete_load_balancer.called


def test_list_load_balancers_rejects_invalid_pagination(client: KrutrimClient) -> None:
    with pytest.raises(ValueError, match="page"):
        client.lb.list_load_balancers_by_vpc(
            vpc_krn=VPC_KRN,
            page=0,
            k_customer_id=K_CUSTOMER_ID,
            x_account_id=X_ACCOUNT_ID,
            x_region=X_REGION,
        )

    with pytest.raises(ValueError, match="limit"):
        client.lb.list_load_balancers_by_vpc(
            vpc_krn=VPC_KRN,
            limit=0,
            k_customer_id=K_CUSTOMER_ID,
            x_account_id=X_ACCOUNT_ID,
            x_region=X_REGION,
        )
