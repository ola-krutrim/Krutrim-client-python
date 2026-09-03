# Omni Sandbox

Omni Sandbox provides isolated, short-lived compute through the normal `KrutrimClient` and `AsyncKrutrimClient`. Authentication comes from the client's bearer API key; sandbox calls do not accept backend identity headers.

## Managed workflow

Use `client.sandbox.create` for the common workflow. It creates the sandbox, waits until its state is `active`, and returns a handle whose helpers automatically bind the sandbox ID.

```python
import json

from krutrim_client import KrutrimClient

with KrutrimClient() as client:
    with client.sandbox.create(
        flavor_name="Omni-CPU-1x-4GB",
        region="In-Bangalore-2",
        timeout=900,
    ) as sandbox:
        sandbox.files.make_dir("/app/work")
        sandbox.files.write("/app/work/input.json", json.dumps({"value": 21}))
        sandbox.files.write(
            "/app/work/program.py",
            "import json\n"
            "data = json.load(open('input.json'))\n"
            "json.dump({'result': data['value'] * 2}, open('output.json', 'w'))\n",
        )
        execution = sandbox.run_command(
            "python3 program.py",
            cwd="/app/work",
            timeout=120,
        )
        if execution.exit_code != 0 or execution.timed_out:
            raise RuntimeError(f"command failed: {execution.stderr}")

        output = sandbox.files.read("/app/work/output.json")
        assert isinstance(output, str)
        print(json.loads(output))
```

The context manager requests asynchronous deletion on every exit. It guarantees that deletion was accepted, not that cluster cleanup has finished. If the body raises and cleanup also fails, the body exception remains primary and the cleanup failure is attached as diagnostic information. Call `sandbox.kill()` for explicit cleanup; repeated calls on the same handle are safe. After an accepted create, the managed readiness loop tolerates temporary not-found responses until the sandbox is first visible. A later disappearance remains an error, and `client.sandbox.connect(sandbox_id)` stays strict because it has no preceding create acknowledgement.

The async API has the same shape:

```python
from krutrim_client import AsyncKrutrimClient

async with AsyncKrutrimClient() as client:
    async with await client.sandbox.create(
        flavor_name="Omni-CPU-1x-4GB",
        region="In-Bangalore-2",
        timeout=900,
    ) as sandbox:
        await sandbox.files.write("/app/message.txt", "hello")
        result = await sandbox.run_command("cat message.txt", cwd="/app")
        print(result.stdout)
```

## Discovery and exact API access

Discover available compute and runtime choices before creating a sandbox:

```python
flavors = client.sandbox.api.list_flavors(region="In-Bangalore-2")
templates = client.sandbox.api.list_templates()
```

The managed facade intentionally polls readiness. For contract-shaped response envelopes and immediate HTTP 202 creation, use `client.sandbox.api`:

```python
accepted = client.sandbox.api.create(
    sandbox_name="batch-worker",
    region="In-Bangalore-2",
    flavor_name="Omni-CPU-1x-4GB",
    template_name="python-runtime-sandbox",
    ttl_seconds=900,
)
print(accepted.data.id, accepted.data.status)
```

All low-level lifecycle, filesystem, command, and port operations have sync/async normal, raw-response, and streaming-response views. Binary downloads and proxy calls use binary response classes:

```python
response = client.with_raw_response.sandbox.api.files.download(
    sandbox.sandbox_id,
    path="/app/archive.bin",
)
response.write_to_file("archive.bin")

with client.with_streaming_response.sandbox.api.files.download(
    sandbox.sandbox_id,
    path="/app/large.bin",
) as response:
    response.stream_to_file("large.bin")
```

## Timeout meanings

Sandbox operations use distinct timeout concepts:

- `client.sandbox.create(timeout=900)` sets sandbox lifetime and sends `ttlSeconds=900`.
- `wait_timeout=300` is the monotonic total deadline for create/connect readiness polling.
- `request_timeout=30` controls individual HTTP calls made by the managed facade.
- `sandbox.run_command(..., timeout=120)` sends the command execution deadline as `timeoutSeconds=120`.
- When command `request_timeout` is omitted, the managed helper uses `timeout + 30` seconds so the transport does not normally expire first.
- `sandbox.set_timeout(900)` resets the expiry deadline to now plus 900 seconds; it is not additive.

The low-level API retains contract-oriented names: `ttl_seconds`, `timeout_seconds`, and the standard SDK request option `timeout`.

## Files, commands, ports, and proxying

`sandbox.files.write` accepts UTF-8 `str`, exact `bytes`, a binary file object, or a local path-like object. Uploads are limited to 100 MB. `sandbox.files.read(path)` decodes UTF-8 and propagates `UnicodeDecodeError`; pass `format="bytes"` for exact bytes. The helper also provides `remove`, `list`, `stat`, `rename`, and `make_dir`.

Command results are data even when the program fails. Inspect `stdout`, `stderr`, `exit_code`, `stdout_truncated`, `stderr_truncated`, and `timed_out`; non-zero exit codes and server-side command timeouts do not raise SDK exceptions. Commands may be 1–100,000 characters and use a 1–270 second execution timeout.

Ports 1024–65535 can be opened, listed, and closed through `sandbox.ports`. Opening returns either the already-open HTTP 200 state or the HTTP 202 provisioning state. The SDK does not hide activation polling: list ports until the requested port reports `active` before routing traffic.

`sandbox.proxy.request(method, path, ...)` forwards GET, POST, PUT, PATCH, DELETE, HEAD, or OPTIONS and returns exact bytes. Paths are relative to the sandbox and traversal segments are rejected. JSON and raw content are mutually exclusive, and request bodies are limited to 100 MB. Proxy calls default to `max_retries=0` so a non-idempotent workload is never repeated silently; opt in explicitly when safe. HTTP failures preserve the SDK's normal `APIStatusError` subclasses and response object. Use the raw/streaming low-level views when headers or incremental response bytes are needed.

## Exceptions and lifecycle limits

HTTP failures continue to use the existing SDK hierarchy, such as `NotFoundError`, `ConflictError`, and `APITimeoutError`. Managed readiness failures raise `SandboxException`; a readiness deadline raises `SandboxTimeoutError`. Both include `sandbox_id` and the last known metadata when available.

The service contract currently specifies: TTL 60–604,800 seconds, at most 10 network-storage attachments, files and proxy bodies up to 100 MB, directory depth 1–10, command timeout 1–270 seconds, ports 1024–65535, and at most 20 open ports per sandbox. Stateful rules such as region/flavor compatibility and active-only operations are enforced by the service.

## Public-gateway assumptions

The implementation follows the supplied `openapi-backend.yaml`, with these deployment assumptions recorded for live verification:

- The public gateway accepts the same bearer `Authorization` header injected by `KrutrimClient`; no account, customer, or backend-only identity headers are required.
- `CreateSandboxRequest` exposes `templateId` and `templateName`, although one schema description says template fields are not accepted. The SDK follows the actual properties and endpoint narrative, enforces mutual exclusivity, and leaves support validation to the deployed service.
- The proxy path is documented as preserving every HTTP method even though the formal path item declares only GET. The SDK supports the standard methods listed above; non-GET routing must be confirmed against the approved deployed gateway.

Run the credential-gated live smoke test before release to confirm these assumptions in the target environment.
