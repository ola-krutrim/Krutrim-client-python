from __future__ import annotations

import io
import re
import json
from typing import Any, Callable, Iterator
from pathlib import Path

import anyio
import httpx
import pytest

import krutrim_client
from krutrim_client import KrutrimClient, AsyncKrutrimClient
from krutrim_client._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

SANDBOX_ID = "57863027-0a7f-4e31-bea9-b0b9dec906cf"
BASE_URL = "https://sandbox.test"


def json_response(request: httpx.Request, payload: object, status_code: int = 200) -> httpx.Response:
    return httpx.Response(status_code, json=payload, request=request)


def active_response(*, status: str = "active") -> dict[str, object]:
    return {
        "status": 200,
        "message": "ok",
        "data": {
            "id": SANDBOX_ID,
            "name": "test-sandbox",
            "krn": "krn:sandbox:test",
            "status": status,
            "region": "test-region",
            "flavorName": "cpu-1",
        },
    }


def create_response() -> dict[str, object]:
    return {
        "status": 202,
        "message": "accepted",
        "data": {
            "id": SANDBOX_ID,
            "name": "test-sandbox",
            "krn": "krn:sandbox:test",
            "status": "deploying",
            "region": "test-region",
        },
    }


def make_client(
    handler: Callable[[httpx.Request], httpx.Response],
    *,
    max_retries: int = 0,
) -> KrutrimClient:
    return KrutrimClient(
        api_key="test-key",
        base_url=BASE_URL,
        max_retries=max_retries,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def make_async_client(
    handler: Callable[[httpx.Request], httpx.Response],
    *,
    max_retries: int = 0,
) -> AsyncKrutrimClient:
    client = AsyncKrutrimClient(
        api_key="test-key",
        base_url=BASE_URL,
        max_retries=max_retries,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )
    # Avoid the SDK's existing platform-detection worker thread in this test
    # environment; MockTransport tests do not need runtime platform probing.
    client._platform = "Linux"
    return client


async def test_public_client_surface_and_exports() -> None:
    client = make_client(lambda request: json_response(request, {}))
    async_client = make_async_client(lambda request: json_response(request, {}))
    try:
        assert client.sandbox.api.files is client.sandbox.api.files
        assert client.sandbox.api.commands is client.sandbox.api.commands
        assert client.sandbox.api.ports is client.sandbox.api.ports
        assert client.sandbox.api.proxy is client.sandbox.api.proxy
        assert client.copy().sandbox
        assert client.with_options().sandbox
        assert client.with_raw_response.sandbox.api.files
        assert client.with_streaming_response.sandbox.api.files

        assert async_client.sandbox.api.files is async_client.sandbox.api.files
        assert async_client.copy().sandbox
        assert async_client.with_options().sandbox
        assert async_client.with_raw_response.sandbox.api.files
        assert async_client.with_streaming_response.sandbox.api.files

        assert krutrim_client.Sandbox
        assert krutrim_client.AsyncSandbox
        assert issubclass(krutrim_client.SandboxException, krutrim_client.KrutrimClientError)
        assert issubclass(krutrim_client.SandboxTimeoutError, krutrim_client.SandboxException)
    finally:
        client.close()
        await async_client.close()


def test_sync_low_level_lifecycle_paths_aliases_and_wrappers() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        path = request.url.path
        if path == "/omni/sandbox/v1/template":
            return json_response(request, [{"ID": 7, "template_name": "python", "supported_services": ["sandbox"]}])
        if path == "/omni/sandbox/v1/flavors":
            return json_response(request, {"status": 200, "data": [{"name": "cpu-1", "subject": "test-region"}]})
        if path == "/omni/sandbox/v1/sandbox" and request.method == "GET":
            return json_response(request, {"status": 200, "data": {"rows": [], "total": 0, "totalPages": 0}})
        if path == "/omni/sandbox/v1/sandbox" and request.method == "POST":
            return json_response(request, create_response(), 202)
        if path.endswith("/ttl"):
            return json_response(
                request,
                {"status": 200, "data": {"id": SANDBOX_ID, "ttlSeconds": 900, "expiresAt": "2030-01-01T00:00:00Z"}},
            )
        if path.endswith(SANDBOX_ID) and request.method == "GET":
            return json_response(request, active_response())
        if path.endswith(SANDBOX_ID) and request.method == "DELETE":
            return json_response(request, {"status": 202, "data": {"id": SANDBOX_ID}}, 202)
        raise AssertionError(f"unexpected request: {request.method} {path}")

    with make_client(handler) as client:
        assert client.sandbox.api.list_templates()[0].id == 7
        assert client.sandbox.api.list_flavors(region="test-region").data[0].name == "cpu-1"  # type: ignore[index,union-attr]
        listed = client.sandbox.api.list(region="test-region", status="active", name="x", page=1, limit=20)
        assert listed.data is not None and listed.data.total_pages == 0
        created = client.sandbox.api.create(
            sandbox_name="test-sandbox",
            region="test-region",
            flavor_name="cpu-1",
            template_name="python",
            network_storages=[{"network_storage_id": "storage-1", "network_storage_mount_path": "/app/data"}],
            environment_variables={"TOKEN": "ZW5jb2RlZA=="},
            ttl_seconds=900,
        )
        assert created.status == 202
        assert client.sandbox.api.retrieve(SANDBOX_ID).data.status == "active"  # type: ignore[union-attr]
        assert client.sandbox.api.set_ttl(SANDBOX_ID, 900).data.ttl_seconds == 900  # type: ignore[union-attr]
        assert client.sandbox.api.delete(SANDBOX_ID).status == 202

        raw = client.with_raw_response.sandbox.api.create(
            sandbox_name="test-sandbox",
            region="test-region",
            flavor_name="cpu-1",
        )
        assert raw.status_code == 202
        assert raw.parse().data.id == SANDBOX_ID  # type: ignore[union-attr]
        with client.with_streaming_response.sandbox.api.create(
            sandbox_name="test-sandbox",
            region="test-region",
            flavor_name="cpu-1",
        ) as streamed:
            assert streamed.status_code == 202
            assert streamed.parse().data.id == SANDBOX_ID  # type: ignore[union-attr]

    list_request = requests[2]
    assert dict(list_request.url.params) == {
        "region": "test-region",
        "status": "active",
        "name": "x",
        "page": "1",
        "limit": "20",
    }
    create_request = requests[3]
    body = json.loads(create_request.content)
    assert body == {
        "sandboxName": "test-sandbox",
        "region": "test-region",
        "flavorName": "cpu-1",
        "templateName": "python",
        "networkStorages": [{"networkStorageId": "storage-1", "networkStorageMountPath": "/app/data"}],
        "environmentVariables": {"TOKEN": "ZW5jb2RlZA=="},
        "ttlSeconds": 900,
    }
    assert requests[0].headers["authorization"] == "Bearer test-key"
    assert json.loads(requests[5].content) == {"ttlSeconds": 900}


async def test_async_low_level_lifecycle_parity_and_immediate_create() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/omni/sandbox/v1/sandbox" and request.method == "POST":
            return json_response(request, create_response(), 202)
        if request.url.path.endswith(SANDBOX_ID):
            return json_response(request, active_response())
        raise AssertionError(str(request.url))

    async with make_async_client(handler) as client:
        created = await client.sandbox.api.create(
            sandbox_name="test-sandbox",
            region="test-region",
            flavor_name="cpu-1",
            template_id=7,
        )
        assert created.status == 202
        assert len(requests) == 1
        assert json.loads(requests[0].content)["templateId"] == 7
        raw = await client.with_raw_response.sandbox.api.retrieve(SANDBOX_ID)
        assert (await raw.parse()).data.status == "active"  # type: ignore[union-attr]
        async with client.with_streaming_response.sandbox.api.retrieve(SANDBOX_ID) as streamed:
            assert (await streamed.parse()).data.status == "active"  # type: ignore[union-attr]


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda api: api.create(sandbox_name="Bad_Name", region="r", flavor_name="f"), "DNS-1035"),
        (
            lambda api: api.create(
                sandbox_name="valid", region="r", flavor_name="f", template_id=1, template_name="python"
            ),
            "mutually exclusive",
        ),
        (
            lambda api: api.create(
                sandbox_name="valid",
                region="r",
                flavor_name="f",
                network_storages=[{"network_storage_id": str(index)} for index in range(11)],
            ),
            "at most 10",
        ),
        (lambda api: api.create(sandbox_name="valid", region="r", flavor_name="f", ttl_seconds=59), "between 60"),
        (lambda api: api.retrieve(""), "non-empty"),
        (lambda api: api.list(page=0), "at least 1"),
        (lambda api: api.list(limit=101), "between 1 and 100"),
    ],
)
def test_low_level_lifecycle_validation(call: Callable[[Any], object], message: str) -> None:
    client = make_client(lambda request: (_ for _ in ()).throw(AssertionError(request)))
    with client:
        with pytest.raises(ValueError, match=message):
            call(client.sandbox.api)


def test_sync_managed_create_connect_lifecycle_and_timeout_mapping() -> None:
    requests: list[httpx.Request] = []
    retrieve_states = iter(["deploying", "active", "active"])

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/omni/sandbox/v1/sandbox" and request.method == "POST":
            return json_response(request, create_response(), 202)
        if request.url.path.endswith(SANDBOX_ID) and request.method == "GET":
            return json_response(request, active_response(status=next(retrieve_states)))
        raise AssertionError(f"unexpected request: {request.method} {request.url.path}")

    with make_client(handler) as client:
        sleeps: list[float] = []
        client.sandbox._sleep = sleeps.append
        sandbox = client.sandbox.create(
            sandbox_name="test-sandbox",
            region="test-region",
            flavor_name="cpu-1",
            timeout=900,
            request_timeout=30,
        )
        assert sandbox.sandbox_id == SANDBOX_ID
        assert sandbox.sandbox_krn == "krn:sandbox:test"
        assert sandbox.metadata.status == "active"
        assert sleeps == [0.25]
        connected = client.sandbox.connect(SANDBOX_ID)
        assert connected.sandbox_id == SANDBOX_ID

    create_request = requests[0]
    assert json.loads(create_request.content)["ttlSeconds"] == 900
    assert create_request.extensions["timeout"]["read"] == 30
    assert len([request for request in requests if request.method == "POST"]) == 1


def test_sync_create_retries_initial_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    states: Iterator[str | None] = iter([None, "deploying", "active"])

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return json_response(request, create_response(), 202)
        state = next(states)
        if state is None:
            return json_response(request, {"message": "not visible yet"}, 404)
        return json_response(request, active_response(status=state))

    with make_client(handler) as client:
        sleeps: list[float] = []
        monkeypatch.setattr(client.sandbox, "_sleep", sleeps.append)
        sandbox = client.sandbox.create(region="test-region", flavor_name="cpu-1")
        assert sandbox.metadata.status == "active"
        assert sleeps == [0.25, 0.5]

    disappearing_states: Iterator[str | None] = iter(["deploying", None])

    def disappearing(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return json_response(request, create_response(), 202)
        state = next(disappearing_states)
        if state is None:
            return json_response(request, {"message": "gone"}, 404)
        return json_response(request, active_response(status=state))

    with make_client(disappearing) as client:
        monkeypatch.setattr(client.sandbox, "_sleep", lambda _: None)
        with pytest.raises(krutrim_client.SandboxException, match="disappeared"):
            client.sandbox.create(region="test-region", flavor_name="cpu-1")

    def never_visible(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return json_response(request, create_response(), 202)
        return json_response(request, {"message": "not visible yet"}, 404)

    with make_client(never_visible) as client:
        monkeypatch.setattr(client.sandbox, "_sleep", lambda _: None)
        with pytest.raises(krutrim_client.SandboxTimeoutError) as exc_info:
            client.sandbox.create(region="test-region", flavor_name="cpu-1", wait_timeout=0.000001)
        assert exc_info.value.metadata is None


def test_generated_name_and_managed_failure_states() -> None:
    captured_names: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            captured_names.append(json.loads(request.content)["sandboxName"])
            return json_response(request, create_response(), 202)
        return json_response(
            request,
            {
                **active_response(status="failed_deploy"),
                "data": {**active_response(status="failed_deploy")["data"], "errorMessage": "image failed"},  # type: ignore[dict-item]
            },
        )

    with make_client(handler) as client:
        with pytest.raises(krutrim_client.SandboxException, match="image failed") as exc_info:
            client.sandbox.create(region="test-region", flavor_name="cpu-1")
        assert exc_info.value.sandbox_id == SANDBOX_ID
    assert re.fullmatch(r"sandbox-[0-9a-f]{12}", captured_names[0])


def test_managed_disappearance_and_deadline() -> None:
    def missing(request: httpx.Request) -> httpx.Response:
        return json_response(request, {"message": "gone"}, 404)

    with make_client(missing) as client:
        with pytest.raises(krutrim_client.SandboxException, match="disappeared"):
            client.sandbox.connect(SANDBOX_ID)

    def deploying(request: httpx.Request) -> httpx.Response:
        return json_response(request, active_response(status="deploying"))

    with make_client(deploying) as client:
        client.sandbox._sleep = lambda _: None
        with pytest.raises(krutrim_client.SandboxTimeoutError) as exc_info:
            client.sandbox.connect(SANDBOX_ID, wait_timeout=0.000001)
        assert exc_info.value.metadata.status == "deploying"


async def test_async_managed_wait_uses_async_sleep() -> None:
    states = iter(["deploying", "active"])

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return json_response(request, create_response(), 202)
        return json_response(request, active_response(status=next(states)))

    async with make_async_client(handler) as client:
        sleeps: list[float] = []

        async def fake_sleep(delay: float) -> None:
            sleeps.append(delay)

        client.sandbox._sleep = fake_sleep
        sandbox = await client.sandbox.create(region="test-region", flavor_name="cpu-1")
        assert sandbox.sandbox_id == SANDBOX_ID
        assert sleeps == [0.25]


async def test_async_create_retries_initial_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    states: Iterator[str | None] = iter([None, "deploying", "active"])

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return json_response(request, create_response(), 202)
        state = next(states)
        if state is None:
            return json_response(request, {"message": "not visible yet"}, 404)
        return json_response(request, active_response(status=state))

    async with make_async_client(handler) as client:
        sleeps: list[float] = []

        async def fake_sleep(delay: float) -> None:
            sleeps.append(delay)

        monkeypatch.setattr(client.sandbox, "_sleep", fake_sleep)
        sandbox = await client.sandbox.create(region="test-region", flavor_name="cpu-1")
        assert sandbox.metadata.status == "active"
        assert sleeps == [0.25, 0.5]


def test_handle_lifecycle_bound_caching_and_context_cleanup() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "GET":
            return json_response(request, active_response())
        if request.url.path.endswith("/ttl"):
            return json_response(
                request,
                {"status": 200, "data": {"id": SANDBOX_ID, "ttlSeconds": 1200, "expiresAt": "2030-01-01T00:00:00Z"}},
            )
        return json_response(request, {"status": 202, "data": {"id": SANDBOX_ID}}, 202)

    with make_client(handler) as client:
        sandbox = client.sandbox.connect(SANDBOX_ID)
        assert sandbox.files is sandbox.files
        assert sandbox.commands is sandbox.commands
        assert sandbox.ports is sandbox.ports
        assert sandbox.proxy is sandbox.proxy
        sandbox.set_timeout(1200)
        assert sandbox.metadata.ttl_seconds == 1200
        assert sandbox.is_running()
        with sandbox as entered:
            assert entered is sandbox
        sandbox.kill()

    deletes = [request for request in requests if request.method == "DELETE"]
    assert len(deletes) == 1


def test_context_manager_exception_precedence() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            return json_response(request, active_response())
        return json_response(request, {"message": "cleanup failed"}, 500)

    with make_client(handler) as client:
        sandbox = client.sandbox.connect(SANDBOX_ID)
        with pytest.raises(RuntimeError, match="body failed") as exc_info:
            with sandbox:
                raise RuntimeError("body failed")
        assert isinstance(exc_info.value.__sandbox_cleanup_error__, krutrim_client.InternalServerError)


async def test_async_context_cleanup_and_idempotent_kill() -> None:
    deletes = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal deletes
        if request.method == "GET":
            return json_response(request, active_response())
        deletes += 1
        return json_response(request, {"status": 202}, 202)

    async with make_async_client(handler) as client:
        sandbox = await client.sandbox.connect(SANDBOX_ID)
        async with sandbox as entered:
            assert entered is sandbox
        await sandbox.kill()
    assert deletes == 1


def test_sync_files_exact_content_bound_helpers_and_binary_wrappers(tmp_path: Path) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "GET" and request.url.path.endswith(SANDBOX_ID):
            return json_response(request, active_response())
        if request.method == "GET" and request.url.path.endswith("/files"):
            path = request.url.params["path"]
            content = b"\xff" if path == "/bad" else "hello".encode()
            return httpx.Response(
                200, content=content, request=request, headers={"Content-Type": "application/octet-stream"}
            )
        if request.url.path.endswith("/files/list"):
            return json_response(request, {"status": 200, "data": [{"name": "a", "path": "/a", "type": "file"}]})
        if request.url.path.endswith("/files/stat"):
            return json_response(request, {"status": 200, "data": {"name": "a", "path": "/a", "type": "file"}})
        return json_response(request, {"status": 200, "data": {"path": request.url.params.get("path"), "type": "file"}})

    local_file = tmp_path / "payload.bin"
    local_file.write_bytes(b"from-path")
    with make_client(handler) as client:
        api = client.sandbox.api.files
        api.upload(SANDBOX_ID, path="/bytes", content=b"\x00\xff")
        api.upload(SANDBOX_ID, path="/stream", content=io.BytesIO(b"stream"))
        api.upload(SANDBOX_ID, path="/path", content=local_file)
        assert api.download(SANDBOX_ID, path="/hello") == b"hello"
        assert api.list(SANDBOX_ID, path="/", depth=2).data[0].name == "a"  # type: ignore[index,union-attr]
        assert api.stat(SANDBOX_ID, path="/a").data.name == "a"  # type: ignore[union-attr]
        api.move(SANDBOX_ID, path="/a", new_path="/b")
        api.make_directory(SANDBOX_ID, path="/dir")
        api.delete(SANDBOX_ID, path="/b")

        sandbox = client.sandbox.connect(SANDBOX_ID)
        sandbox.files.write("/text", "snowman: ☃")
        assert sandbox.files.read("/hello") == "hello"
        assert sandbox.files.read("/hello", format="bytes") == b"hello"
        assert sandbox.files.list("/")[0].name == "a"
        assert sandbox.files.stat("/a").name == "a"
        sandbox.files.rename("/a", "/b")
        sandbox.files.make_dir("/dir")
        sandbox.files.remove("/b")
        with pytest.raises(UnicodeDecodeError):
            sandbox.files.read("/bad")
        with pytest.raises(ValueError, match="format"):
            sandbox.files.read("/hello", format="xml")  # type: ignore[arg-type]

        raw = client.with_raw_response.sandbox.api.files.download(SANDBOX_ID, path="/hello")
        assert isinstance(raw, BinaryAPIResponse)
        assert raw.read() == b"hello"
        with client.with_streaming_response.sandbox.api.files.download(SANDBOX_ID, path="/hello") as streamed:
            assert isinstance(streamed, StreamedBinaryAPIResponse)
            assert b"".join(streamed.iter_bytes()) == b"hello"

    uploads = [request for request in requests if request.method == "POST" and request.url.path.endswith("/files")]
    assert [request.content for request in uploads[:3]] == [b"\x00\xff", b"stream", b"from-path"]
    assert uploads[0].headers["content-type"] == "application/octet-stream"
    text_upload = next(request for request in uploads if request.url.params["path"] == "/text")
    assert text_upload.content == "snowman: ☃".encode()
    move = next(request for request in requests if request.url.path.endswith("/files/move"))
    assert dict(move.url.params) == {"path": "/a", "newPath": "/b"}


async def test_async_files_and_binary_wrappers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    uploads: list[bytes] = []
    offloaded: list[str] = []

    async def fake_path_read_bytes(path: anyio.Path) -> bytes:
        offloaded.append(str(path))
        return b"path-data"

    async def fake_run_sync(function: Callable[[], bytes]) -> bytes:
        offloaded.append("binary-file")
        return function()

    monkeypatch.setattr(anyio.Path, "read_bytes", fake_path_read_bytes)
    monkeypatch.setattr(anyio.to_thread, "run_sync", fake_run_sync)

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET" and request.url.path.endswith("/files"):
            return httpx.Response(200, content=b"async", request=request)
        if request.method == "GET" and request.url.path.endswith(SANDBOX_ID):
            return json_response(request, active_response())
        uploads.append(request.content)
        return json_response(request, {"status": 200, "data": {"path": request.url.params.get("path")}})

    local_file = tmp_path / "async.bin"
    local_file.write_bytes(b"path-data")
    async with make_async_client(handler) as client:
        await client.sandbox.api.files.upload(SANDBOX_ID, path="/path", content=local_file)
        await client.sandbox.api.files.upload(SANDBOX_ID, path="/stream", content=io.BytesIO(b"stream-data"))
        sandbox = await client.sandbox.connect(SANDBOX_ID)
        await sandbox.files.write("/text", "async-text")
        assert await sandbox.files.read("/file") == "async"
        raw = await client.with_raw_response.sandbox.api.files.download(SANDBOX_ID, path="/file")
        assert isinstance(raw, AsyncBinaryAPIResponse)
        assert await raw.read() == b"async"
        async with client.with_streaming_response.sandbox.api.files.download(SANDBOX_ID, path="/file") as streamed:
            assert isinstance(streamed, AsyncStreamedBinaryAPIResponse)
            assert b"".join([chunk async for chunk in streamed.iter_bytes()]) == b"async"
    assert uploads[:3] == [b"path-data", b"stream-data", b"async-text"]
    assert offloaded == [str(local_file), "binary-file"]


def test_file_validation_and_size_limit() -> None:
    client = make_client(lambda request: (_ for _ in ()).throw(AssertionError(request)))
    with client:
        with pytest.raises(ValueError, match="non-empty"):
            client.sandbox.api.files.upload(SANDBOX_ID, path="", content=b"x")
        with pytest.raises(ValueError, match="depth"):
            client.sandbox.api.files.list(SANDBOX_ID, depth=11)
        with pytest.raises(ValueError, match="100 MB"):
            client.sandbox.api.files.upload(SANDBOX_ID, path="/big", content=b"x" * (100 * 1024 * 1024 + 1))
        with pytest.raises(TypeError, match="binary"):
            client.sandbox.api.files.upload(SANDBOX_ID, path="/text", content=io.StringIO("bad"))  # type: ignore[arg-type]


def test_commands_bound_alias_results_and_timeouts() -> None:
    requests: list[httpx.Request] = []
    results = iter(
        [
            {
                "stdout": "ok",
                "stderr": "",
                "exitCode": 0,
                "stdoutTruncated": False,
                "stderrTruncated": False,
                "timedOut": False,
            },
            {
                "stdout": "partial",
                "stderr": "boom",
                "exitCode": 7,
                "stdoutTruncated": True,
                "stderrTruncated": False,
                "timedOut": False,
            },
            {
                "stdout": "partial",
                "stderr": "",
                "exitCode": -1,
                "stdoutTruncated": False,
                "stderrTruncated": False,
                "timedOut": True,
            },
        ]
    )

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "GET":
            return json_response(request, active_response())
        return json_response(request, {"status": 200, "data": next(results)})

    with make_client(handler) as client:
        sandbox = client.sandbox.connect(SANDBOX_ID)
        result = sandbox.commands.run("echo ok", cwd="/app", envs={"A": "B"}, timeout=120)
        assert result.stdout == "ok" and result.exit_code == 0
        nonzero = sandbox.run_command("exit 7", timeout=10, request_timeout=11)
        assert nonzero.exit_code == 7 and nonzero.stdout_truncated
        timed_out = sandbox.run_command("sleep 2", timeout=1)
        assert timed_out.timed_out and timed_out.exit_code == -1

    first = requests[1]
    assert json.loads(first.content) == {"cmd": "echo ok", "cwd": "/app", "envs": {"A": "B"}, "timeoutSeconds": 120}
    assert first.extensions["timeout"]["read"] == 150
    assert requests[2].extensions["timeout"]["read"] == 11


async def test_async_command_parity() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.method == "GET":
            return json_response(request, active_response())
        return json_response(request, {"status": 200, "data": {"stdout": "ok", "exitCode": 0}})

    async with make_async_client(handler) as client:
        sandbox = await client.sandbox.connect(SANDBOX_ID)
        result = await sandbox.run_command("pwd", timeout=20)
        assert result.stdout == "ok"
    assert json.loads(requests[-1].content)["timeoutSeconds"] == 20
    assert requests[-1].extensions["timeout"]["read"] == 50


@pytest.mark.parametrize(
    ("command", "timeout"),
    [("", 60), ("x" * 100001, 60), ("ok", 0), ("ok", 271)],
    ids=["empty", "too-long", "timeout-low", "timeout-high"],
)
def test_command_validation(command: str, timeout: int) -> None:
    client = make_client(lambda request: (_ for _ in ()).throw(AssertionError(request)))
    with client:
        with pytest.raises(ValueError):
            client.sandbox.api.commands.run(SANDBOX_ID, command, timeout_seconds=timeout)


def test_ports_and_proxy_bound_id_preservation_and_no_retries() -> None:
    requests: list[httpx.Request] = []
    proxy_failures = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal proxy_failures
        requests.append(request)
        path = request.url.path
        if request.method == "GET" and path.endswith(SANDBOX_ID):
            return json_response(request, active_response())
        if path.endswith("/ports") and request.method == "POST":
            return json_response(request, {"status": 202, "data": {"port": 3000, "status": "provisioning"}}, 202)
        if path.endswith("/ports") and request.method == "GET":
            return json_response(
                request, {"status": 200, "data": [{"port": 3000, "status": "active", "url": "/route"}]}
            )
        if "/ports/" in path:
            return httpx.Response(202, request=request)
        if path.endswith("/retry"):
            proxy_failures += 1
            return json_response(request, {"message": "failed"}, 500)
        return httpx.Response(200, content=b"proxied", request=request, headers={"X-Upstream": "yes"})

    with make_client(handler, max_retries=2) as client:
        client._sleep = lambda _: None
        sandbox = client.sandbox.connect(SANDBOX_ID)
        opened = sandbox.ports.open(3000)
        assert opened.status == "provisioning"
        assert sandbox.ports.list()[0].status == "active"
        sandbox.ports.close(3000)
        assert (
            sandbox.proxy.request(
                "POST",
                "/api/items",
                query={"page": 2},
                headers={"X-Custom": "value"},
                content=b"\x00body",
            )
            == b"proxied"
        )
        with pytest.raises(krutrim_client.InternalServerError):
            sandbox.proxy.request("GET", "/retry")

        raw = client.with_raw_response.sandbox.api.proxy.request(SANDBOX_ID, "GET", "/health")
        assert isinstance(raw, BinaryAPIResponse)
        assert raw.read() == b"proxied"
        with client.with_streaming_response.sandbox.api.proxy.request(SANDBOX_ID, "GET", "/health") as streamed:
            assert isinstance(streamed, StreamedBinaryAPIResponse)
            assert b"".join(streamed.iter_bytes()) == b"proxied"

    port_requests = [request for request in requests if "/ports" in request.url.path]
    assert [request.method for request in port_requests] == ["POST", "GET", "DELETE"]
    proxied = next(request for request in requests if request.url.path.endswith("/api/items"))
    assert proxied.method == "POST"
    assert dict(proxied.url.params) == {"page": "2"}
    assert proxied.headers["x-custom"] == "value"
    assert proxied.content == b"\x00body"
    assert proxy_failures == 1


async def test_async_ports_proxy_and_raw_streaming_parity() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        path = request.url.path
        if request.method == "GET" and path.endswith(SANDBOX_ID):
            return json_response(request, active_response())
        if path.endswith("/ports"):
            return json_response(request, {"status": 200, "data": {"port": 8080, "status": "active"}})
        return httpx.Response(200, content=b"async-proxy", request=request)

    async with make_async_client(handler) as client:
        sandbox = await client.sandbox.connect(SANDBOX_ID)
        assert (await sandbox.ports.open(8080)).port == 8080
        assert await sandbox.proxy.request("GET", "/health") == b"async-proxy"
        raw = await client.with_raw_response.sandbox.api.proxy.request(SANDBOX_ID, "GET", "/health")
        assert isinstance(raw, AsyncBinaryAPIResponse)
        assert await raw.read() == b"async-proxy"
        async with client.with_streaming_response.sandbox.api.proxy.request(SANDBOX_ID, "GET", "/health") as streamed:
            assert isinstance(streamed, AsyncStreamedBinaryAPIResponse)
            assert b"".join([chunk async for chunk in streamed.iter_bytes()]) == b"async-proxy"


@pytest.mark.parametrize(
    "call",
    [
        lambda api: api.ports.open(SANDBOX_ID, 1023),
        lambda api: api.ports.close(SANDBOX_ID, 65536),
        lambda api: api.proxy.request(SANDBOX_ID, "TRACE", "/"),
        lambda api: api.proxy.request(SANDBOX_ID, "GET", "/../secret"),
        lambda api: api.proxy.request(SANDBOX_ID, "POST", "/", json={}, content=b"x"),
        lambda api: api.proxy.request(SANDBOX_ID, "POST", "/", content=b"x" * (100 * 1024 * 1024 + 1)),
    ],
)
def test_port_and_proxy_validation(call: Callable[[Any], object]) -> None:
    client = make_client(lambda request: (_ for _ in ()).throw(AssertionError(request)))
    with client:
        with pytest.raises(ValueError):
            call(client.sandbox.api)


def test_low_level_status_errors_are_preserved() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return json_response(request, {"message": "conflict"}, 409)

    with make_client(handler) as client:
        with pytest.raises(krutrim_client.ConflictError) as exc_info:
            client.sandbox.api.ports.open(SANDBOX_ID, 3000)
        assert exc_info.value.response.status_code == 409
