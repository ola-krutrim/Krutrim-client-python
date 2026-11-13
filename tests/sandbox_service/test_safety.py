from __future__ import annotations

import json
import asyncio
from typing import Any, Iterator, AsyncIterator
from unittest.mock import patch
from typing_extensions import override

import anyio
import httpx
import pytest

from krutrim_client import (
    KrutrimClient,
    APIStatusError,
    AsyncKrutrimClient,
    SandboxStreamError,
    AuthenticationError,
    SandboxOperationError,
    SandboxOperationTimeoutError,
)
from krutrim_client._models import FinalRequestOptions
from krutrim_client.types.sandbox_service import ExecErrorEvent

from .test_contract import OP, KRN, BASE, SBOX, BINARY, REGION, UPLOAD


@pytest.fixture(autouse=True)
def credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KRUTRIMCLIENT_API_KEY", "test-token")


def operation(state: str = "succeeded") -> httpx.Response:
    return httpx.Response(
        200, json={"code": "Operation.Get", "details": {**OP, "state": state, "error": "backend failed"}}
    )


def sandbox() -> httpx.Response:
    return httpx.Response(200, json={"code": "Sandbox.Extend", "details": SBOX})


@pytest.mark.parametrize("async_mode", [False, True])
@pytest.mark.parametrize("key_source", ["generated", "explicit", "headers", "defaults"])
async def test_stable_retry_keys(async_mode: bool, key_source: str) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if len(requests) == 1:
            raise httpx.ReadError("lost acknowledgement")
        if len(requests) == 2:
            return httpx.Response(503, json={"error": "transient"})
        return sandbox()

    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    http_cls: Any = httpx.AsyncClient if async_mode else httpx.Client
    kwargs: dict[str, Any] = {
        "base_url": BASE,
        "http_client": http_cls(transport=httpx.MockTransport(handle)),
        "max_retries": 2,
    }
    if key_source == "defaults":
        kwargs["default_headers"] = {"IDEMPOTENCY-KEY": "same-key"}
    client: Any = cls(**kwargs)
    call_args: dict[str, Any] = {"krn_id": KRN, "x_region": REGION, "ttl_seconds": 60}
    if key_source == "explicit":
        call_args["idempotency_key"] = "same-key"
    if key_source == "headers":
        call_args["extra_headers"] = {"iDeMpOtEnCy-KeY": "same-key"}
    with patch.object(client, "_calculate_retry_timeout", return_value=0):
        response = client.sandbox.sandboxes.extend(**call_args)
        if async_mode:
            response = await response
    assert response.details.krn_id == KRN
    assert len(requests) == 3
    assert len({r.headers["idempotency-key"] for r in requests}) == 1
    assert len({r.content for r in requests}) == 1
    assert all(len(r.headers.get_list("idempotency-key")) == 1 for r in requests)
    if key_source != "generated":
        assert requests[0].headers["idempotency-key"] == "same-key"
    if async_mode:
        await client.close()
    else:
        client.close()


@pytest.mark.parametrize("async_mode", [False, True])
async def test_generated_key_is_new_for_each_action(async_mode: bool) -> None:
    keys: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        keys.append(request.headers["idempotency-key"])
        return sandbox()

    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    http_cls: Any = httpx.AsyncClient if async_mode else httpx.Client
    client: Any = cls(base_url=BASE, http_client=http_cls(transport=httpx.MockTransport(handle)))
    for _ in range(2):
        result = client.sandbox.sandboxes.extend(krn_id=KRN, x_region=REGION, ttl_seconds=60)
        if async_mode:
            await result
    assert len(set(keys)) == 2
    if async_mode:
        await client.close()
    else:
        client.close()


@pytest.mark.parametrize("method", ["upload", "exec_stream", "create_ticket"])
@pytest.mark.parametrize("failure", ["network", "status"])
@pytest.mark.parametrize("async_mode", [False, True])
async def test_unsafe_calls_never_retry(method: str, failure: str, async_mode: bool) -> None:
    count = 0

    def handle(_request: httpx.Request) -> httpx.Response:
        nonlocal count
        count += 1
        if failure == "network":
            raise httpx.ConnectError("connection failed")
        return httpx.Response(503, json={"error": "unavailable"})

    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    http_cls: Any = httpx.AsyncClient if async_mode else httpx.Client
    client: Any = cls(base_url=BASE, max_retries=3, http_client=http_cls(transport=httpx.MockTransport(handle)))
    target = {
        "upload": client.sandbox.files.upload,
        "exec_stream": client.sandbox.sandboxes.exec_stream,
        "create_ticket": client.sandbox.terminal.create_ticket,
    }[method]
    kwargs = {"upload": {"path": "/tmp/x", "content": b"x"}, "exec_stream": {"cmd": "echo hi"}, "create_ticket": {}}[
        method
    ]
    with pytest.raises(Exception) as exc:
        result = target(krn_id=KRN, x_region=REGION, **kwargs)
        if async_mode:
            await result
    assert not isinstance(exc.value, AssertionError)
    assert count == 1
    if async_mode:
        await client.close()
    else:
        client.close()


@pytest.mark.parametrize("method", ["upload", "exec_stream", "create_ticket"])
@pytest.mark.parametrize("async_mode", [False, True])
async def test_unsafe_calls_reject_header_keys(method: str, async_mode: bool) -> None:
    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    client: Any = cls(base_url=BASE, default_headers={"IDEMPOTENCY-KEY": "unsafe"})
    target = {
        "upload": client.sandbox.files.upload,
        "exec_stream": client.sandbox.sandboxes.exec_stream,
        "create_ticket": client.sandbox.terminal.create_ticket,
    }[method]
    kwargs = {"upload": {"path": "/tmp/x", "content": b"x"}, "exec_stream": {"cmd": "echo hi"}, "create_ticket": {}}[
        method
    ]
    with pytest.raises(ValueError, match="Idempotency-Key"):
        result = target(krn_id=KRN, x_region=REGION, **kwargs)
        if async_mode:
            await result
    if async_mode:
        await client.close()
    else:
        client.close()


@pytest.mark.parametrize(
    "body,status,exception",
    [
        ({"error": "invalid token", "code": "invalid_token"}, 401, AuthenticationError),
        (
            {"code": "Sandbox.Get", "message": "denied", "details": {"error": "denied", "code": "missing_token"}},
            401,
            AuthenticationError,
        ),
        ({"code": "Sandbox.Create", "message": "credits", "details": {"error": "credits"}}, 402, APIStatusError),
        ({"code": "File.Upload", "details": {"error": "too big"}}, 413, APIStatusError),
        ({"error": "forbidden"}, 403, APIStatusError),
    ],
)
@pytest.mark.parametrize("async_mode", [False, True])
async def test_error_bodies_preserved(
    body: dict[str, Any], status: int, exception: type[APIStatusError], async_mode: bool
) -> None:
    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    http_cls: Any = httpx.AsyncClient if async_mode else httpx.Client
    client: Any = cls(
        base_url=BASE,
        max_retries=0,
        http_client=http_cls(transport=httpx.MockTransport(lambda _: httpx.Response(status, json=body))),
    )
    with pytest.raises(exception) as caught:
        result = client.sandbox.sandboxes.retrieve(krn_id=KRN, x_region=REGION)
        if async_mode:
            await result
    assert caught.value.body == body
    assert caught.value.status_code == status
    if async_mode:
        await client.close()
    else:
        client.close()


@pytest.mark.parametrize("async_mode", [False, True])
@pytest.mark.parametrize("state", ["succeeded", "failed", "running"])
async def test_waiter(async_mode: bool, state: str) -> None:
    count = 0
    clock = [0.0]

    def handle(request: httpx.Request) -> httpx.Response:
        nonlocal count
        count += 1
        assert 0 < request.extensions["timeout"]["read"] <= 3
        return operation("pending" if count == 1 else state)

    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    http_cls: Any = httpx.AsyncClient if async_mode else httpx.Client
    client: Any = cls(base_url=BASE, http_client=http_cls(transport=httpx.MockTransport(handle)))

    def sleep(_self: object, seconds: float) -> None:
        clock[0] += seconds

    async def asleep(_self: object, seconds: float) -> None:
        clock[0] += seconds

    from krutrim_client.resources.sandbox_service.operations import OperationsResource, AsyncOperationsResource

    resource_cls = AsyncOperationsResource if async_mode else OperationsResource
    # Patch this module's time object, not the process monotonic clock used by the async scheduler.
    with patch("krutrim_client.resources.sandbox_service.operations.time") as timer, patch.object(
        resource_cls, "_sleep", asleep if async_mode else sleep
    ):
        timer.monotonic.side_effect = lambda: clock[0]
        if state == "succeeded":
            result = client.sandbox.operations.wait("op-1", x_region=REGION, timeout_seconds=3, poll_interval_seconds=1)
            if async_mode:
                result = await result
            assert result.details.state == "succeeded"
        else:
            expected = SandboxOperationError if state == "failed" else SandboxOperationTimeoutError
            with pytest.raises(expected) as exc:
                result = client.sandbox.operations.wait(
                    "op-1", x_region=REGION, timeout_seconds=3, poll_interval_seconds=1
                )
                if async_mode:
                    await result
            assert exc.value.operation is not None
            assert exc.value.operation.details.id == "op-1"
    assert count == (3 if state == "running" else 2)
    if async_mode:
        await client.close()
    else:
        client.close()


async def test_waiter_async_deadline_and_cancellation() -> None:
    cancelled = asyncio.Event()
    started = asyncio.Event()

    async def handle(_: httpx.Request) -> httpx.Response:
        started.set()
        try:
            await anyio.sleep(10)
        finally:
            cancelled.set()
        return operation()

    async with AsyncKrutrimClient(
        base_url=BASE, http_client=httpx.AsyncClient(transport=httpx.MockTransport(handle))
    ) as client:
        with pytest.raises(SandboxOperationTimeoutError):
            await client.sandbox.operations.wait("op-1", x_region=REGION, timeout_seconds=0.01)
        assert cancelled.is_set()
        cancelled.clear()
        started.clear()
        task = asyncio.create_task(client.sandbox.operations.wait("op-1", x_region=REGION))
        await started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert cancelled.is_set()


@pytest.mark.parametrize("async_mode", [False, True])
async def test_waiter_http_errors_propagate_without_retries(async_mode: bool) -> None:
    count = 0

    def handle(_: httpx.Request) -> httpx.Response:
        nonlocal count
        count += 1
        return httpx.Response(503, json={"error": "unavailable"})

    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    http_cls: Any = httpx.AsyncClient if async_mode else httpx.Client
    client: Any = cls(base_url=BASE, max_retries=3, http_client=http_cls(transport=httpx.MockTransport(handle)))
    with pytest.raises(APIStatusError):
        result = client.sandbox.operations.wait("op-1", x_region=REGION)
        if async_mode:
            await result
    assert count == 1
    assert not hasattr(client.sandbox.operations.with_raw_response, "wait")
    if async_mode:
        await client.close()
    else:
        client.close()


class ChunkStream(httpx.SyncByteStream, httpx.AsyncByteStream):
    def __init__(self, chunks: list[bytes], broken: bool = False) -> None:
        self.chunks = chunks
        self.broken = broken
        self.closed = False

    @override
    def __iter__(self) -> Iterator[bytes]:
        yield from self.chunks
        if self.broken:
            raise httpx.ReadError("truncated transfer")

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        for chunk in self.chunks:
            yield chunk
        if self.broken:
            raise httpx.ReadError("truncated transfer")

    @override
    def close(self) -> None:
        self.closed = True

    @override
    async def aclose(self) -> None:
        self.closed = True


@pytest.mark.parametrize("async_mode", [False, True])
@pytest.mark.parametrize("scenario", ["normal", "error", "eof", "disconnect", "malformed", "early_close"])
async def test_stream_events_and_cleanup(async_mode: bool, scenario: str) -> None:
    output = ': keepalive\r\n\r\nevent: stdout\r\ndata: {"data":"नमस्ते"}\r\n\r\nevent: stderr\ndata: {"data":"oops"}\n\n'.encode()
    endings = {
        "normal": b'event: exit\ndata: {"exit_code":2,"timed_out":false,"duration_ms":3.25}\n\n',
        "error": b'event: error\ndata: {"error":"exec broke"}\n\n',
        "eof": b"",
        "disconnect": b"",
        "malformed": b"event: stdout\ndata: not-json\n\n",
        "early_close": b"",
    }
    raw = output + endings[scenario]
    stream = ChunkStream([raw[i : i + 1] for i in range(len(raw))], broken=scenario == "disconnect")
    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    http_cls: Any = httpx.AsyncClient if async_mode else httpx.Client
    client: Any = cls(
        base_url=BASE,
        http_client=http_cls(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(200, stream=stream, headers={"content-type": "text/event-stream"})
            )
        ),
    )
    events: list[Any] = []

    async def consume_async() -> None:
        result = await client.sandbox.sandboxes.exec_stream(krn_id=KRN, x_region=REGION, cmd="test")
        async with result:
            async for event in result:
                events.append(event)
                if scenario == "early_close":
                    break

    def consume_sync() -> None:
        result = client.sandbox.sandboxes.exec_stream(krn_id=KRN, x_region=REGION, cmd="test")
        with result:
            for event in result:
                events.append(event)
                if scenario == "early_close":
                    break

    if scenario in ("normal", "early_close"):
        if async_mode:
            await consume_async()
        else:
            consume_sync()
    else:
        with pytest.raises(SandboxStreamError) as caught:
            if async_mode:
                await consume_async()
            else:
                consume_sync()
        assert caught.value.response is not None
        if scenario == "error":
            assert isinstance(caught.value.event, ExecErrorEvent)
            assert caught.value.event.type == "error"
    assert events[0].type == "stdout" and events[0].data == "नमस्ते"
    if scenario != "early_close":
        assert events[1].type == "stderr"
    if scenario == "normal":
        assert events[-1].type == "exit" and events[-1].exit_code == 2
    assert stream.closed
    if async_mode:
        await client.close()
    else:
        client.close()


@pytest.mark.parametrize("async_mode", [False, True])
@pytest.mark.parametrize("content", [b"", BINARY, "chunks"])
async def test_raw_uploads(async_mode: bool, content: Any) -> None:
    expected = BINARY if content == "chunks" else content

    async def chunks() -> AsyncIterator[bytes]:
        yield BINARY[:2]
        yield BINARY[2:]

    payload = (
        chunks()
        if content == "chunks" and async_mode
        else iter([BINARY[:2], BINARY[2:]])
        if content == "chunks"
        else content
    )

    def handle(request: httpx.Request) -> httpx.Response:
        assert request.content == expected
        assert request.headers["content-type"] == "application/octet-stream"
        return httpx.Response(200, json={"code": "File.Upload", "details": UPLOAD})

    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    http_cls: Any = httpx.AsyncClient if async_mode else httpx.Client
    client: Any = cls(base_url=BASE, http_client=http_cls(transport=httpx.MockTransport(handle)))
    result = client.sandbox.files.upload(krn_id=KRN, x_region=REGION, path="/tmp/x", content=payload)
    if async_mode:
        await result
    if async_mode:
        await client.close()
    else:
        client.close()


@pytest.mark.parametrize("async_mode", [False, True])
async def test_interrupted_download_propagates(async_mode: bool) -> None:
    stream = ChunkStream([BINARY[:2]], broken=True)
    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    http_cls: Any = httpx.AsyncClient if async_mode else httpx.Client
    client: Any = cls(
        base_url=BASE,
        http_client=http_cls(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(
                    200, stream=stream, headers={"content-type": "application/octet-stream", "content-length": "4"}
                )
            )
        ),
    )
    if async_mode:
        with pytest.raises(httpx.ReadError):
            async with client.sandbox.files.with_streaming_response.download(
                krn_id=KRN, x_region=REGION, path="/tmp/x"
            ) as response:
                _ = [part async for part in response.iter_bytes()]
        await client.close()
    else:
        with pytest.raises(httpx.ReadError):
            with client.sandbox.files.with_streaming_response.download(
                krn_id=KRN, x_region=REGION, path="/tmp/x"
            ) as response:
                list(response.iter_bytes())
        client.close()
    assert stream.closed


@pytest.mark.parametrize(
    "resource,method,kwargs",
    [
        ("sandboxes", "create", dict(name="bad name", flavor="small")),
        ("sandboxes", "create", dict(name="ok", flavor="small", template="python", image="node")),
        ("sandboxes", "create", dict(name="ok", flavor="small", env={"SPACE_X": "secret"})),
        ("sandboxes", "extend", dict(krn_id=KRN, ttl_seconds=59)),
        ("sandboxes", "extend", dict(krn_id=KRN, ttl_seconds=True)),
        ("sandboxes", "exec", dict(krn_id=KRN, cmd="x", timeout_seconds=121)),
        ("sandboxes", "exec", dict(krn_id=KRN, cmd="x", cwd="relative")),
        ("sandboxes", "exec", dict(krn_id=KRN, cmd="x", stdin="é" * 524289)),
        ("sandboxes", "exec", dict(krn_id=KRN, cmd="x", extra_body={"stream": True})),
        ("sandboxes", "exec", dict(krn_id=KRN, cmd="x", env={"bad-name": "x"})),
        ("sandboxes", "exec_stream", dict(krn_id=KRN, cmd="x", timeout_seconds=3601)),
        ("sandboxes", "list", dict(limit=201)),
        ("sandboxes", "list", dict(status="DELETED")),
        ("sandboxes", "retrieve", dict(krn_id="")),
        ("templates", "create", dict(name="img-reserved", image="python")),
        ("templates", "retrieve", dict(template_id="..")),
        ("commands", "create", dict(krn_id=KRN, cmd="x", env={"KRUTRIM_X": "secret"})),
        ("commands", "retrieve", dict(krn_id=KRN, command_id="cmd-1", stdout_offset=-1)),
        ("ports", "expose", dict(krn_id=KRN, port=65536)),
        ("ports", "close", dict(krn_id=KRN, port=0)),
        ("files", "download", dict(krn_id=KRN, path="relative")),
        ("files", "download", dict(krn_id=KRN, path="/" + "é" * 128)),
        ("network", "update", dict(krn_id=KRN, network={"egress": {"default_action": "bad"}})),
        (
            "network",
            "update",
            dict(krn_id=KRN, network={"egress": {"default_action": "deny", "allow": ["https://a.com"]}}),
        ),
        ("sandboxes", "extend", dict(krn_id=KRN, ttl_seconds=60, idempotency_key="has space")),
    ],
)
@pytest.mark.parametrize("async_mode", [False, True])
async def test_validation_before_http(resource: str, method: str, kwargs: dict[str, Any], async_mode: bool) -> None:
    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    client: Any = cls(base_url=BASE)
    with pytest.raises(ValueError):
        result = getattr(getattr(client.sandbox, resource), method)(x_region=REGION, **kwargs)
        if async_mode:
            await result
    if async_mode:
        await client.close()
    else:
        client.close()


def test_raw_content_cannot_mix_with_json_or_multipart() -> None:
    with KrutrimClient(base_url=BASE) as client:
        extras: list[dict[str, Any]] = [
            {"json_data": {"x": 1}},
            {"extra_json": {"x": 1}},
            {"files": {"file": ("file", b"bytes")}},
        ]
        for extra in extras:
            with pytest.raises(ValueError, match="Cannot provide raw content"):
                client._build_request(FinalRequestOptions.construct(method="put", url="/x", content=b"bytes", **extra))


def test_existing_json_and_multipart_requests_unchanged() -> None:
    with KrutrimClient(base_url=BASE) as client:
        json_request = client._build_request(
            FinalRequestOptions.construct(method="post", url="/x", json_data={"name": "hello"})
        )
        assert json.loads(json_request.read()) == {"name": "hello"}
        multipart = client._build_request(
            FinalRequestOptions.construct(
                method="post",
                url="/x",
                files={"file": ("test.bin", BINARY)},
                json_data={"name": "test"},
                headers={"Content-Type": "multipart/form-data"},
            )
        )
        assert BINARY in multipart.read()
        assert "multipart/form-data; boundary=" in multipart.headers["content-type"]


def test_network_reset_and_extra_options() -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        assert json.loads(request.content) == {}
        assert request.headers.get_list("x-region") == [REGION]
        return httpx.Response(
            202,
            json={"code": "Network.Update", "details": {"enforcement": {"status": "pending"}, "operation_id": "op-1"}},
        )

    with KrutrimClient(
        base_url=BASE,
        default_headers={"X-Region": "old"},
        http_client=httpx.Client(transport=httpx.MockTransport(handle)),
    ) as client:
        client.sandbox.network.update(krn_id=KRN, x_region=REGION, network={})


async def test_async_exec_cancellation_closes_connection() -> None:
    started = asyncio.Event()

    class WaitingStream(httpx.AsyncByteStream):
        closed = False

        @override
        async def __aiter__(self) -> AsyncIterator[bytes]:
            yield b'event: stdout\ndata: {"data":"started"}\n\n'
            started.set()
            await anyio.sleep(10)

        @override
        async def aclose(self) -> None:
            await anyio.sleep(0)
            self.closed = True

    body = WaitingStream()
    async with AsyncKrutrimClient(
        base_url=BASE,
        http_client=httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(200, stream=body, headers={"content-type": "text/event-stream"})
            )
        ),
    ) as client:

        async def consume() -> None:
            stream = await client.sandbox.sandboxes.exec_stream(krn_id=KRN, x_region=REGION, cmd="long job")
            async with stream:
                async for _event in stream:
                    pass

        task = asyncio.create_task(consume())
        await started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert body.closed


@pytest.mark.parametrize("async_mode", [False, True])
async def test_streaming_download_does_not_read_until_iteration(async_mode: bool) -> None:
    consumed: list[bool] = []

    class LazyStream(ChunkStream):
        @override
        def __iter__(self) -> Iterator[bytes]:
            consumed.append(True)
            yield from super().__iter__()

        @override
        async def __aiter__(self) -> AsyncIterator[bytes]:
            consumed.append(True)
            async for chunk in super().__aiter__():
                yield chunk

    body = LazyStream([BINARY])
    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    http_cls: Any = httpx.AsyncClient if async_mode else httpx.Client
    client: Any = cls(
        base_url=BASE,
        http_client=http_cls(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(200, stream=body, headers={"content-type": "application/octet-stream"})
            )
        ),
    )
    if async_mode:
        async with client.sandbox.files.with_streaming_response.download(
            krn_id=KRN, x_region=REGION, path="/tmp/x"
        ) as response:
            assert not consumed
            assert await response.read() == BINARY
        await client.close()
    else:
        with client.sandbox.files.with_streaming_response.download(
            krn_id=KRN, x_region=REGION, path="/tmp/x"
        ) as response:
            assert not consumed
            assert response.read() == BINARY
        client.close()
    assert consumed and body.closed


def test_upload_content_type_overrides_differently_cased_defaults() -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        assert request.headers.get_list("content-type") == ["application/octet-stream"]
        assert request.content == b"literal file"
        return httpx.Response(200, json={"code": "File.Upload", "details": UPLOAD})

    with KrutrimClient(
        base_url=BASE,
        default_headers={"content-type": "application/json"},
        http_client=httpx.Client(transport=httpx.MockTransport(handle)),
    ) as client:
        client.sandbox.files.upload(krn_id=KRN, x_region=REGION, path="/tmp/x", content=b"literal file")


@pytest.mark.parametrize("async_mode", [False, True])
async def test_error_before_exec_stream_is_http_error(async_mode: bool) -> None:
    cls: Any = AsyncKrutrimClient if async_mode else KrutrimClient
    http_cls: Any = httpx.AsyncClient if async_mode else httpx.Client
    error = {"code": "Sandbox.Exec", "details": {"error": "sandbox is DOWN"}}
    client: Any = cls(
        base_url=BASE, http_client=http_cls(transport=httpx.MockTransport(lambda _: httpx.Response(409, json=error)))
    )
    with pytest.raises(APIStatusError) as exc:
        result = client.sandbox.sandboxes.exec_stream(krn_id=KRN, x_region=REGION, cmd="echo x")
        if async_mode:
            await result
    assert exc.value.body == error
    if async_mode:
        await client.close()
    else:
        client.close()
