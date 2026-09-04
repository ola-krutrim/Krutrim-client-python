from __future__ import annotations

import os
import time

import pytest

from krutrim_client import KrutrimClient

LIVE_ENABLED = os.environ.get("KRUTRIM_SANDBOX_LIVE") == "1"
pytestmark = pytest.mark.skipif(not LIVE_ENABLED, reason="set KRUTRIM_SANDBOX_LIVE=1 to run live sandbox smoke")

WORKSPACE = "/app/sdk-live-smoke"
PORT = 18765

SERVER = """\
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def do_POST(self):
        length = int(self.headers.get("content-length", "0"))
        body = self.rfile.read(length)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass

HTTPServer(("0.0.0.0", 18765), Handler).serve_forever()
"""


def required_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.skip(f"set {name} to run live sandbox smoke")
    return value


def test_live_sandbox_workflow_and_proxy() -> None:
    with KrutrimClient() as client:
        with client.sandbox.create(
            flavor_name=required_environment("KRUTRIM_SANDBOX_FLAVOR"),
            region=required_environment("KRUTRIM_SANDBOX_REGION"),
            timeout=900,
            wait_timeout=300,
        ) as sandbox:
            assert sandbox.is_running()
            sandbox.files.make_dir(WORKSPACE)
            sandbox.files.write(f"{WORKSPACE}/input.txt", "sandbox-live")
            result = sandbox.run_command("cp input.txt output.txt", cwd=WORKSPACE)
            assert result.exit_code == 0
            assert sandbox.files.read(f"{WORKSPACE}/output.txt") == "sandbox-live"

            sandbox.files.write(f"{WORKSPACE}/server.py", SERVER)
            started = sandbox.run_command(
                "python3 server.py >server.log 2>&1 &",
                cwd=WORKSPACE,
            )
            assert started.exit_code == 0
            sandbox.ports.open(PORT)

            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                if any(item.port == PORT and item.status == "active" for item in sandbox.ports.list()):
                    break
                time.sleep(0.5)
            else:
                raise AssertionError("sandbox smoke-test port did not become active")

            assert sandbox.proxy.request("GET", f"/port/{PORT}/health") == b"ok"
            assert sandbox.proxy.request("POST", f"/port/{PORT}/echo", content=b"payload") == b"payload"
