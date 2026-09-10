# Lifecycle, discovery, and TTL control

Own the sandbox lifecycle explicitly: discover what you can create, create
without a context manager, reattach by ID, extend the TTL, and delete
deliberately. This is the pattern for sandboxes shared across processes or
kept alive beyond one code block.

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

1. Lists compute flavors for the region (`client.sandbox.api.list_flavors`)
   and runtime templates (`client.sandbox.api.list_templates`).
2. Creates a sandbox with `client.sandbox.create(..., timeout=300)` — no
   `with` block, so deletion is handled in `try/finally`.
3. Prints the handle's `metadata`: status, flavor, `ttl_seconds`,
   `expires_at`.
4. Reattaches with `client.sandbox.connect(sandbox_id)` — how a second
   process picks up an existing sandbox — and runs a command through the
   reconnected handle.
5. Checks `is_running()` and extends the lifetime with `set_timeout(900)`,
   which resets expiry to now + 900 s (not additive); the handle's metadata
   updates in place.
6. Deletes explicitly with `kill()` (idempotent), then polls `is_running()`
   until the asynchronous deletion completes.

## Run

```bash
python main.py
```

Expected output:

```
Flavors in In-Bangalore-1 (<n> total):
  - sandbox-nano
  - ...
Templates (<n> total):
  - ...

Created: <sandbox-id>
  status:     active
  flavor:     <flavor>
  ttl:        300 seconds
  expires at: <timestamp>

Reconnected handle says: hello from a reconnected handle
Running: True
Expires at after set_timeout(900): <later timestamp>

Sandbox deleted, is_running() -> False
```
