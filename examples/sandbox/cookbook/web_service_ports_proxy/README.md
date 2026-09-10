# Web service with ports and proxy

Run an HTTP service inside a sandbox and call it from outside — through the
authenticated SDK proxy and via the port's public URL.

## Prerequisites

```bash
pip install krutrim-client
export KRUTRIMCLIENT_API_KEY="<your-api-key>"
export KRUTRIM_SANDBOX_REGION="In-Bangalore-1"
export KRUTRIM_SANDBOX_FLAVOR="sandbox-large"
```

See [../../README.md](../../README.md) for flavor discovery and
[../../../../docs/sandbox.md](../../../../docs/sandbox.md) for the full guide.

## What it does

`main.py` starts a stdlib JSON API inside the sandbox as a background process, then:

1. Opens port 8000 with `sandbox.ports.open` and polls `sandbox.ports.list()`
   until the port is `active` — required before any traffic reaches the
   service.
2. Polls `sandbox.proxy.request("GET", "/port/8000/health")` until the server
   answers. Proxy paths are prefixed with `/port/{port}/` and carry the SDK's
   authentication.
3. Sends `POST /port/8000/predict` through the proxy and prints the JSON
   response.
4. Prints the port's public URL (anyone with the link can call it directly).
5. Closes the port; the `with` block deletes the sandbox.

## Run

```bash
python main.py
```

Expected output:

```
Sandbox active: <sandbox-id>
Server ready (via proxy): {'status': 'ok'}
Prediction (via proxy): {'prediction': 42}
Public URL: https://<gateway-host>/omni/sandbox/v1/<sandbox-id>/port/8000/
Port closed.
```
