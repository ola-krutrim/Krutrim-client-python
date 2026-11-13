from __future__ import annotations

import json
import time
import threading
from typing import Any, Iterator
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing_extensions import override

import httpx
import pytest

from krutrim_client import KrutrimClient, AsyncKrutrimClient, SandboxOperationTimeoutError
from krutrim_client.types.sandbox_service import NetworkResponse

REGION = "In-Bangalore-1"


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("reset", [False, True])
async def test_network_policy_update_response(asynchronous: bool, reset: bool) -> None:
    policy: dict[str, Any] = {} if reset else {"egress": {"default_action": "deny", "allow": ["example.com"]}}
    details = {**policy, "enforcement": {"status": "pending"}, "operation_id": "op-network"}

    def handle(request: httpx.Request) -> httpx.Response:
        assert json.loads(request.content) == policy
        return httpx.Response(202, json={"code": "Network.Update", "details": details})

    client: Any = (
        AsyncKrutrimClient(
            api_key="test",
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(handle)),
            _strict_response_validation=True,
        )
        if asynchronous
        else KrutrimClient(
            api_key="test",
            http_client=httpx.Client(transport=httpx.MockTransport(handle)),
            _strict_response_validation=True,
        )
    )
    try:
        result = client.sandbox.network.update(krn_id="krn-test", x_region=REGION, network=policy)
        if asynchronous:
            result = await result
        assert isinstance(result, NetworkResponse)
        assert result.details.enforcement is not None
        assert result.details.enforcement.status == "pending"
        assert result.details.operation_id == "op-network"
        if reset:
            assert result.details.egress is None
        else:
            assert result.details.egress is not None
            assert result.details.egress.allow == ["example.com"]
    finally:
        if asynchronous:
            await client.close()
        else:
            client.close()


@pytest.fixture
def trickle_server() -> Iterator[tuple[str, threading.Event]]:
    closed = threading.Event()

    class Handler(BaseHTTPRequestHandler):
        @override
        def log_message(self, format: str, *args: Any) -> None:
            del format, args

        def do_GET(self) -> None:
            body = json.dumps(
                {
                    "code": "Operation.Get",
                    "details": {
                        "id": "op-trickle",
                        "type": "create",
                        "state": "running",
                        "attempts": 1,
                        "account_id": "a",
                        "customer_id": "c",
                        "region": REGION,
                        "created_at": 1.0,
                        "updated_at": 2.0,
                    },
                }
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body) + 20))
            self.end_headers()
            try:
                # Every read makes progress well within the per-read timeout.
                for _ in range(20):
                    self.wfile.write(b" ")
                    self.wfile.flush()
                    time.sleep(0.03)
                self.wfile.write(body)
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                closed.set()

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", closed
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_sync_wait_deadline_covers_progressing_response(trickle_server: tuple[str, threading.Event]) -> None:
    url, closed = trickle_server
    with KrutrimClient(api_key="offline-placeholder", base_url=url) as client:
        started = time.monotonic()
        with pytest.raises(SandboxOperationTimeoutError) as error:
            client.sandbox.operations.wait(
                "op-trickle", x_region=REGION, timeout_seconds=0.15, poll_interval_seconds=0.01
            )
        assert time.monotonic() - started < 0.4
        assert error.value.operation_id == "op-trickle"
        assert closed.wait(timeout=1), "abandoned polling response must be closed"


async def test_async_wait_deadline_covers_progressing_response(trickle_server: tuple[str, threading.Event]) -> None:
    url, closed = trickle_server
    async with AsyncKrutrimClient(api_key="offline-placeholder", base_url=url) as client:
        started = time.monotonic()
        with pytest.raises(SandboxOperationTimeoutError):
            await client.sandbox.operations.wait(
                "op-trickle", x_region=REGION, timeout_seconds=0.15, poll_interval_seconds=0.01
            )
        assert time.monotonic() - started < 0.4
    assert closed.wait(timeout=1)


def test_sync_wait_closes_progressing_custom_transport() -> None:
    closed = threading.Event()

    class ProgressStream(httpx.SyncByteStream):
        @override
        def __iter__(self) -> Iterator[bytes]:
            while True:
                time.sleep(0.01)
                yield b" "

        @override
        def close(self) -> None:
            closed.set()

    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/json"}, stream=ProgressStream())

    with KrutrimClient(api_key="test", http_client=httpx.Client(transport=httpx.MockTransport(handle))) as client:
        with pytest.raises(SandboxOperationTimeoutError):
            client.sandbox.operations.wait("op-1", x_region=REGION, timeout_seconds=0.05)
        assert closed.wait(timeout=0.5)
