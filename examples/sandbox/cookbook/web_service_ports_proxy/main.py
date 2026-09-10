"""Cookbook: run a web service inside a sandbox and call it from outside.

1. Open a port and poll until it is `active` (required before any traffic).
2. Call the service from this host via `sandbox.proxy.request` using the
   `/port/{PORT}/...` path prefix — authenticated SDK access, no public URL
   needed by the caller.
3. Share the port's public URL for direct browser/HTTP access.

The service is a small stdlib-only JSON API started in the background, so
`run_command` returns immediately and the sandbox keeps serving requests.
"""

from __future__ import annotations

import os
import json
import time
from urllib.parse import urljoin

from krutrim_client import KrutrimClient, APIStatusError

WORKSPACE = "/app/work"
PORT = 8000
READY_DEADLINE = 60  # seconds to wait for server start / port activation


def required_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Set {name} before running this example")
    return value


def server_program() -> str:
    """A stdlib JSON API: GET /health and POST /predict (doubles a value)."""
    return f'''
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {{"status": "ok"}})
        else:
            self._send(404, {{"error": "not found"}})

    def do_POST(self):
        if self.path != "/predict":
            self._send(404, {{"error": "not found"}})
            return
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length) or b"{{}}")
        self._send(200, {{"prediction": data.get("value", 0) * 2}})

    def log_message(self, *args):
        pass

HTTPServer(("0.0.0.0", {PORT}), Handler).serve_forever()
'''


def wait_for_server(sandbox) -> None:  # type: ignore[no-untyped-def]
    """Poll the proxy until the in-sandbox server answers on the active port."""
    deadline = time.monotonic() + READY_DEADLINE
    while True:
        try:
            body = sandbox.proxy.request("GET", f"/port/{PORT}/health")
            print("Server ready (via proxy):", json.loads(body))
            return
        except APIStatusError:
            if time.monotonic() > deadline:
                log = sandbox.run_command("cat server.log", cwd=WORKSPACE, timeout=10)
                raise RuntimeError(
                    f"server did not answer in time:\n{log.stdout}{log.stderr}"
                ) from None
            time.sleep(1)


def wait_for_port_active(sandbox) -> str:  # type: ignore[no-untyped-def]
    """Poll `ports.list` until our port is active, then return its public URL."""
    deadline = time.monotonic() + READY_DEADLINE
    while True:
        for info in sandbox.ports.list():
            if info.port != PORT:
                continue
            if info.status == "active" and info.url:
                return info.url
            if info.status == "failed":
                raise RuntimeError(f"port {PORT} failed to activate: {info.error_message}")
        if time.monotonic() > deadline:
            raise RuntimeError(f"port {PORT} was not active after {READY_DEADLINE} seconds")
        time.sleep(1)


def main() -> None:
    with KrutrimClient() as client:
        with client.sandbox.create(
            flavor_name=required_environment("KRUTRIM_SANDBOX_FLAVOR"),
            region=required_environment("KRUTRIM_SANDBOX_REGION"),
            timeout=900,
        ) as sandbox:
            print("Sandbox active:", sandbox.sandbox_id)

            # 1. Upload the service and start it in the background. The command
            #    returns immediately; the 270 s per-command cap does not apply
            #    to the server's lifetime.
            sandbox.files.make_dir(WORKSPACE)
            sandbox.files.write(f"{WORKSPACE}/server.py", server_program())
            launch = sandbox.run_command(
                "nohup python3 server.py > server.log 2>&1 & echo $! > server.pid",
                cwd=WORKSPACE,
                timeout=10,
            )
            if launch.exit_code != 0:
                raise RuntimeError(f"failed to launch server: {launch.stderr}")

            # 2. Expose the port and wait until it is active. Both proxy and
            #    public-URL traffic require the port to be open.
            sandbox.ports.open(PORT)
            url = wait_for_port_active(sandbox)

            # 3. Call the service through the authenticated SDK proxy. Paths
            #    are prefixed with /port/{PORT}/; the server may still be
            #    booting, so poll /health first.
            wait_for_server(sandbox)
            body = sandbox.proxy.request("POST", f"/port/{PORT}/predict", json={"value": 21})
            print("Prediction (via proxy):", json.loads(body))

            # 4. The same service is also reachable directly at the public URL
            #    by anyone with the link. The service may return the URL as a
            #    gateway-relative path, so join it with the client base URL.
            print("Public URL:", urljoin(str(client.base_url), url))

            # 5. Clean up the exposure; the sandbox itself is deleted by the
            #    context manager on exit.
            sandbox.ports.close(PORT)
            print("Port closed.")


if __name__ == "__main__":
    main()
