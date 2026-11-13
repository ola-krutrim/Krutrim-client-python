"""Pinned customer route contracts, exercised through real SDK HTTP transports."""

from __future__ import annotations

import json
import inspect
from typing import Any, cast

import httpx
import pytest

from krutrim_client import KrutrimClient, AsyncKrutrimClient
from krutrim_client._models import BaseModel
from krutrim_client.types.sandbox_service import (
    ExecResponse,
    PortResponse,
    UsageResponse,
    CommandResponse,
    NetworkResponse,
    SandboxResponse,
    PortListResponse,
    TemplateResponse,
    OperationResponse,
    PortCloseResponse,
    FileUploadResponse,
    FlavorListResponse,
    CommandListResponse,
    SandboxListResponse,
    TemplateListResponse,
    CommandOutputResponse,
    TemplateDeleteResponse,
    TerminalTicketResponse,
)

REGION = "In-Bangalore-1"
KRN = "krn:sandbox:In-Bangalore-1:account:customer:sandbox:uuid"
BASE = "https://sandbox.test"
SBOX = dict(
    krn_id=KRN,
    name="test",
    status="ACTIVE",
    is_deleted=False,
    flavor="sandbox-medium",
    template="base",
    vcpus=1,
    mem_mib=2048,
    ttl_seconds=3600,
    created_at=1.25,
    updated_at=2.5,
    expires_at=3601.25,
    account_id="account",
    customer_id="customer",
    region=REGION,
    env=["GREETING"],
)
OP = dict(
    id="op-1",
    type="create",
    state="succeeded",
    attempts=1,
    account_id="account",
    customer_id="customer",
    region=REGION,
    created_at=1.25,
    updated_at=2.5,
    krn_id=KRN,
)
TEMPLATE = dict(krn_id="krn:template:1", id="python", default_template=True, custom=False, status="active")
COMMAND = dict(command_id="cmd-1", krn_id=KRN, cmd="echo hi", user="user", pid=42, status="running", started_at=1.25)
PORT = dict(
    port=8080,
    access="token",
    created_at=1.25,
    proxy_url="https://sandbox.test/proxy/",
    url="https://sandbox.test/token/",
)
EXEC = dict(krn_id=KRN, stdout="hi\n", stderr="", exit_code=0, duration_ms=5.25)
UPLOAD = dict(name="file.bin", path="/home/user/a & b.bin", size_bytes=4, sha256="abc")
USAGE = dict(
    krn_id=KRN,
    name="test",
    account_id="account",
    customer_id="customer",
    region=REGION,
    metering_status="running",
    running_seconds=1,
    vcpu_seconds=1,
    mem_mib_seconds=2048,
    by_flavor=[],
    intervals=[],
    events=[],
    closed=False,
    updated_at=2.5,
)
PAGE = dict(total=1, limit=5, offset=0)
BINARY = b"\x00\xff{}"
SSE = b'event: stdout\ndata: {"data":"hi"}\n\nevent: exit\ndata: {"exit_code":0,"duration_ms":1.25}\n\n'

# resource, method, HTTP verb, route, arguments, expected body, expected query, response model, details
CASES: list[tuple[Any, ...]] = [
    (
        "sandboxes",
        "create",
        "POST",
        "/sandboxes",
        {"name": "test", "flavor": "sandbox-medium", "env": {"GREETING": "hi"}},
        {"name": "test", "flavor": "sandbox-medium", "env": {"GREETING": "hi"}},
        {},
        SandboxResponse,
        {**SBOX, "operation_id": "op-1"},
    ),
    (
        "sandboxes",
        "list",
        "GET",
        "/sandboxes",
        {"status": "ACTIVE", "name": "test", "limit": 5, "offset": 0},
        None,
        {"status": "ACTIVE", "name": "test", "limit": "5", "offset": "0"},
        SandboxListResponse,
        {**PAGE, "sandboxes": [SBOX]},
    ),
    ("sandboxes", "retrieve", "GET", f"/sandboxes/{KRN}", {"krn_id": KRN}, None, {}, SandboxResponse, SBOX),
    (
        "sandboxes",
        "delete",
        "DELETE",
        f"/sandboxes/{KRN}",
        {"krn_id": KRN},
        {},
        {},
        SandboxResponse,
        {**SBOX, "status": "DELETING", "operation_id": "op-1"},
    ),
    (
        "sandboxes",
        "start",
        "POST",
        f"/sandboxes/{KRN}/start",
        {"krn_id": KRN},
        {},
        {},
        SandboxResponse,
        {**SBOX, "status": "STARTING", "operation_id": "op-1"},
    ),
    (
        "sandboxes",
        "stop",
        "POST",
        f"/sandboxes/{KRN}/stop",
        {"krn_id": KRN},
        {},
        {},
        SandboxResponse,
        {**SBOX, "status": "STOPPING", "operation_id": "op-1"},
    ),
    (
        "sandboxes",
        "extend",
        "POST",
        f"/sandboxes/{KRN}/extend",
        {"krn_id": KRN, "ttl_seconds": 60},
        {"ttl_seconds": 60},
        {},
        SandboxResponse,
        SBOX,
    ),
    (
        "sandboxes",
        "resize",
        "POST",
        f"/sandboxes/{KRN}/resize",
        {"krn_id": KRN, "flavor": "large"},
        {"flavor": "large"},
        {},
        SandboxResponse,
        {**SBOX, "status": "RESIZING", "operation_id": "op-1"},
    ),
    ("sandboxes", "usage", "GET", f"/sandboxes/{KRN}/usage", {"krn_id": KRN}, None, {}, UsageResponse, USAGE),
    (
        "sandboxes",
        "exec",
        "POST",
        f"/sandboxes/{KRN}/exec",
        {
            "krn_id": KRN,
            "cmd": "echo hi",
            "cwd": "/app",
            "env": {"A": "B"},
            "stdin": "hi",
            "user": "1000",
            "timeout_seconds": 30,
        },
        {"cmd": "echo hi", "cwd": "/app", "env": {"A": "B"}, "stdin": "hi", "user": "1000", "timeout_seconds": 30},
        {},
        ExecResponse,
        EXEC,
    ),
    (
        "sandboxes",
        "exec_stream",
        "POST",
        f"/sandboxes/{KRN}/exec",
        {"krn_id": KRN, "cmd": "echo hi", "timeout_seconds": 600},
        {"cmd": "echo hi", "timeout_seconds": 600, "stream": True},
        {},
        None,
        None,
    ),
    (
        "templates",
        "create",
        "POST",
        "/templates",
        {"name": "my-python", "image": "python:3.12", "description": "test"},
        {"name": "my-python", "image": "python:3.12", "description": "test"},
        {},
        TemplateResponse,
        {**TEMPLATE, "operation_id": "op-1"},
    ),
    (
        "templates",
        "list",
        "GET",
        "/templates",
        {"limit": 5, "offset": 0},
        None,
        {"limit": "5", "offset": "0"},
        TemplateListResponse,
        {**PAGE, "templates": [TEMPLATE], "default": "base"},
    ),
    (
        "templates",
        "retrieve",
        "GET",
        "/templates/python",
        {"template_id": "python"},
        None,
        {},
        TemplateResponse,
        TEMPLATE,
    ),
    (
        "templates",
        "delete",
        "DELETE",
        "/templates/python",
        {"template_id": "python"},
        {},
        {},
        TemplateDeleteResponse,
        {"id": "python", "krn_id": "krn:template:1", "status": "deleted"},
    ),
    (
        "flavors",
        "list",
        "GET",
        "/flavors",
        {"limit": 5, "offset": 0},
        None,
        {"limit": "5", "offset": "0"},
        FlavorListResponse,
        {
            **PAGE,
            "flavors": [
                dict(
                    id="small",
                    name="small",
                    vcpus=1,
                    ram_gib=2,
                    local_disk_gib=20,
                    cost=5.61,
                    currency="INR",
                    unit="hour",
                    region=REGION,
                )
            ],
        },
    ),
    ("operations", "retrieve", "GET", "/operations/op-1", {"operation_id": "op-1"}, None, {}, OperationResponse, OP),
    (
        "commands",
        "create",
        "POST",
        f"/sandboxes/{KRN}/commands",
        {"krn_id": KRN, "cmd": "echo hi", "cwd": "/app", "env": {"A": "B"}, "user": "root", "timeout_seconds": 60},
        {"cmd": "echo hi", "cwd": "/app", "env": {"A": "B"}, "user": "root", "timeout_seconds": 60},
        {},
        CommandResponse,
        COMMAND,
    ),
    (
        "commands",
        "list",
        "GET",
        f"/sandboxes/{KRN}/commands",
        {"krn_id": KRN, "limit": 5, "offset": 0},
        None,
        {"limit": "5", "offset": "0"},
        CommandListResponse,
        {**PAGE, "krn_id": KRN, "commands": [COMMAND]},
    ),
    (
        "commands",
        "retrieve",
        "GET",
        f"/sandboxes/{KRN}/commands/cmd-1",
        {"krn_id": KRN, "command_id": "cmd-1", "stdout_offset": 10, "stderr_offset": 20, "max_bytes": 100},
        None,
        {"stdout_offset": "10", "stderr_offset": "20", "max_bytes": "100"},
        CommandOutputResponse,
        dict(
            command=COMMAND, stdout="x", stderr="", stdout_offset=11, stderr_offset=20, stdout_size=11, stderr_size=20
        ),
    ),
    (
        "commands",
        "kill",
        "POST",
        f"/sandboxes/{KRN}/commands/cmd-1/kill",
        {"krn_id": KRN, "command_id": "cmd-1"},
        {},
        {},
        CommandResponse,
        {**COMMAND, "status": "killed"},
    ),
    (
        "files",
        "upload",
        "PUT",
        f"/sandboxes/{KRN}/files",
        {"krn_id": KRN, "path": "/home/user/a & b.bin", "content": BINARY},
        BINARY,
        {"path": "/home/user/a & b.bin"},
        FileUploadResponse,
        UPLOAD,
    ),
    (
        "files",
        "download",
        "GET",
        f"/sandboxes/{KRN}/files",
        {"krn_id": KRN, "path": "/home/user/a & b.bin"},
        None,
        {"path": "/home/user/a & b.bin"},
        None,
        None,
    ),
    (
        "network",
        "retrieve",
        "GET",
        f"/sandboxes/{KRN}/network",
        {"krn_id": KRN},
        None,
        {},
        NetworkResponse,
        {"egress": {"default_action": "deny", "allow": ["pypi.org"]}},
    ),
    (
        "network",
        "update",
        "PUT",
        f"/sandboxes/{KRN}/network",
        {"krn_id": KRN, "network": {"egress": {"default_action": "deny", "allow": ["pypi.org"]}}},
        {"egress": {"default_action": "deny", "allow": ["pypi.org"]}},
        {},
        NetworkResponse,
        {
            "egress": {"default_action": "deny", "allow": ["pypi.org"]},
            "enforcement": {"status": "pending"},
            "operation_id": "op-1",
        },
    ),
    (
        "ports",
        "expose",
        "POST",
        f"/sandboxes/{KRN}/ports",
        {"krn_id": KRN, "port": 8080, "access": "token"},
        {"port": 8080, "access": "token"},
        {},
        PortResponse,
        PORT,
    ),
    (
        "ports",
        "list",
        "GET",
        f"/sandboxes/{KRN}/ports",
        {"krn_id": KRN, "limit": 5, "offset": 0},
        None,
        {"limit": "5", "offset": "0"},
        PortListResponse,
        {**PAGE, "ports": [{k: v for k, v in PORT.items() if k != "url"}]},
    ),
    (
        "ports",
        "close",
        "DELETE",
        f"/sandboxes/{KRN}/ports/8080",
        {"krn_id": KRN, "port": 8080},
        {},
        {},
        PortCloseResponse,
        dict(krn_id=KRN, port=8080, status="closed"),
    ),
    (
        "terminal",
        "create_ticket",
        "POST",
        f"/sandboxes/{KRN}/terminal/ticket",
        {"krn_id": KRN},
        {},
        {},
        TerminalTicketResponse,
        dict(
            krn_id=KRN,
            ticket="ktt_secret",
            url="wss://console.test/?ticket=ktt_secret",
            expires_at="2026-11-03T12:00:00Z",
        ),
    ),
]


def response_for(case: Any) -> httpx.Response:
    if case[1] == "exec_stream":
        return httpx.Response(200, content=SSE, headers={"content-type": "text/event-stream"})
    if case[1] == "download":
        return httpx.Response(
            200,
            content=BINARY,
            headers={"content-type": "application/octet-stream", "content-length": str(len(BINARY))},
        )
    status = 202 if "operation_id" in case[8] else 201 if case[1] in ("expose", "create_ticket") else 200
    return httpx.Response(
        status, json={"code": "Resource.Action", "message": "accepted", "details": case[8]}, headers={"X-Test": "yes"}
    )


def check_request(request: httpx.Request, case: Any) -> None:
    assert request.method == case[2]
    assert request.url.path == "/sandbox/v1" + case[3]
    assert dict(request.url.params) == {**case[6], "custom": "value"}
    assert request.headers["authorization"] == "Bearer secret"
    assert request.headers["x-region"] == REGION
    assert request.headers["x-test-request"] == "yes"
    assert "x-account-id" not in request.headers
    assert "k-customer-id" not in request.headers
    if case[5] is None:
        assert request.content == b""
    elif isinstance(case[5], bytes):
        assert request.content == case[5]
        assert request.headers["content-type"] == "application/octet-stream"
        assert "idempotency-key" not in request.headers
    else:
        assert json.loads(request.content) == case[5]
        if case[1] not in ("exec_stream", "create_ticket"):
            assert request.headers["idempotency-key"]
        else:
            assert "idempotency-key" not in request.headers
    assert request.extensions["timeout"]["read"] == 42


def check_model(result: Any, case: Any) -> None:
    assert isinstance(result, case[7])
    assert isinstance(result.details, BaseModel)
    details = cast(Any, result.details)
    assert result.code == "Resource.Action"
    if case[7] is SandboxResponse:
        assert details.env == ["GREETING"]
        assert details.created_at == 1.25
    if "List" in case[7].__name__:
        assert (details.total, details.limit, details.offset) == (1, 5, 0)
    if case[7] is PortListResponse:
        assert details.ports[0].url is None


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}.{c[1]}" for c in CASES])
@pytest.mark.parametrize("surface", ["normal", "resource_raw", "client_raw", "resource_stream", "client_stream"])
def test_sync_contract(case: Any, surface: str) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        check_request(request, case)
        return response_for(case)

    with KrutrimClient(
        base_url=BASE,
        api_key="secret",
        http_client=httpx.Client(transport=httpx.MockTransport(handle)),
        _strict_response_validation=True,
    ) as client:
        resource = getattr(client.sandbox, case[0])
        if surface == "resource_raw":
            resource = resource.with_raw_response
        if surface == "client_raw":
            resource = getattr(client.with_raw_response.sandbox, case[0])
        if surface == "resource_stream":
            resource = resource.with_streaming_response
        if surface == "client_stream":
            resource = getattr(client.with_streaming_response.sandbox, case[0])
        result = getattr(resource, case[1])(
            **case[4],
            x_region=REGION,
            extra_headers={"x-test-request": "yes"},
            extra_query={"custom": "value"},
            timeout=42,
        )
        if "stream" in surface:
            with result as response:
                result = response if case[1] == "download" else response.parse()
                if case[1] == "download":
                    assert b"".join(result.iter_bytes()) == BINARY
                elif case[1] == "exec_stream":
                    assert [e.type for e in result] == ["stdout", "exit"]
                else:
                    check_model(result, case)
        elif case[1] == "download":
            assert result.read() == BINARY
        else:
            if "raw" in surface:
                result = result.parse()
            if case[1] == "exec_stream":
                with result:
                    assert [e.type for e in result] == ["stdout", "exit"]
            else:
                check_model(result, case)
    assert len(requests) == 1


@pytest.mark.parametrize("case", CASES, ids=[f"{c[0]}.{c[1]}" for c in CASES])
@pytest.mark.parametrize("surface", ["normal", "resource_raw", "client_raw", "resource_stream", "client_stream"])
async def test_async_contract(case: Any, surface: str) -> None:
    requests: list[httpx.Request] = []

    async def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        check_request(request, case)
        return response_for(case)

    async with AsyncKrutrimClient(
        base_url=BASE,
        api_key="secret",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handle)),
        _strict_response_validation=True,
    ) as client:
        resource = getattr(client.sandbox, case[0])
        if surface == "resource_raw":
            resource = resource.with_raw_response
        if surface == "client_raw":
            resource = getattr(client.with_raw_response.sandbox, case[0])
        if surface == "resource_stream":
            resource = resource.with_streaming_response
        if surface == "client_stream":
            resource = getattr(client.with_streaming_response.sandbox, case[0])
        result = getattr(resource, case[1])(
            **case[4],
            x_region=REGION,
            extra_headers={"x-test-request": "yes"},
            extra_query={"custom": "value"},
            timeout=42,
        )
        if "stream" in surface:
            async with result as response:
                result = response if case[1] == "download" else await response.parse()
                if case[1] == "download":
                    assert b"".join([chunk async for chunk in result.iter_bytes()]) == BINARY
                elif case[1] == "exec_stream":
                    assert [e.type async for e in result] == ["stdout", "exit"]
                else:
                    check_model(result, case)
        else:
            if inspect.isawaitable(result):
                result = await result
            if case[1] == "download":
                assert await result.read() == BINARY
            else:
                if "raw" in surface:
                    result = result.parse()
                    if inspect.isawaitable(result):
                        result = await result
                if case[1] == "exec_stream":
                    async with result:
                        assert [e.type async for e in result] == ["stdout", "exit"]
                else:
                    check_model(result, case)
    assert len(requests) == 1
