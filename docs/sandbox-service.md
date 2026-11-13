# Sandbox service APIs (new in 0.8.9)

Use an IAM bearer token with the existing `api_key` option or
`KRUTRIMCLIENT_API_KEY`. Set the gateway **origin** as the client base URL; resource
methods add `/sandbox/v1`. R1 staging uses
`https://r1.staging.olakrutrim.com`. Pass `x_region="In-Bangalore-1"` on each
call. The gateway establishes account/customer identity. The SDK does not send
identity headers on your behalf or refresh expired tokens.

This integration provides the sandbox service customer contract. It includes gateway customer HTTP APIs, SSE exec, and terminal
tickets. Admin, billing, identity/events, WebSocket clients, and arbitrary port
proxy requests are outside this interface.

The existing `client.sandbox.api`, `client.sandbox.create`, and
`client.sandbox.connect` interfaces remain available in this release. They are
planned for deprecation in the next release. The resources below use the new
service contract; they do not redirect existing calls. Import their request and
response types from `krutrim_client.types.sandbox_service`. Existing types under
`krutrim_client.types.sandbox` keep their published meaning.

Production uses `base_url="https://cloud.olakrutrim.com"` (also the existing
public client's default). Existing API-key and base-URL environment aliases
and conflict checks remain supported.

## Resources

All identifiers below are keyword arguments except the operation ID in `wait`.
Use the returned `krn_id` for sandbox calls, not a sandbox name or internal ID.
All HTTP methods also accept `extra_headers`, `extra_query`, and `timeout`;
JSON mutation methods accept `extra_body`. Extra values override method values.

| Resource under `client.sandbox` | Methods and main arguments |
|---|---|
| `sandboxes` | `create(name, flavor, template/image, ttl_seconds, env, network)`, `list(status, name, limit, offset)`, `retrieve(krn_id)`, `delete(krn_id)`, `start(krn_id)`, `stop(krn_id)`, `extend(krn_id, ttl_seconds)`, `resize(krn_id, flavor)`, `usage(krn_id)`, `exec(krn_id, cmd, ...)`, `exec_stream(krn_id, cmd, ...)` |
| `templates` | `create(name, image, description)`, `list(limit, offset)`, `retrieve(template_id)`, `delete(template_id)` |
| `flavors` | `list(limit, offset)` |
| `operations` | `retrieve(operation_id)`, `wait(operation_id, timeout_seconds=600, poll_interval_seconds=2)` |
| `commands` | `create(krn_id, cmd, cwd, env, user, timeout_seconds)`, `list(krn_id, limit, offset)`, `retrieve(krn_id, command_id, stdout_offset, stderr_offset, max_bytes)`, `kill(krn_id, command_id)` |
| `files` | `upload(krn_id, path, content)`, `download(krn_id, path)` |
| `network` | `retrieve(krn_id)`, `update(krn_id, network)` |
| `ports` | `expose(krn_id, port, access)`, `list(krn_id, limit, offset)`, `close(krn_id, port)` |
| `terminal` | `create_ticket(krn_id)` |

Except where required by the method signature, omitted parameters use server
defaults. Lists return one page in `response.details`, including `total`, `limit`,
and `offset`. The default page size is 50; the maximum explicit size is 200.
`limit=0` asks for all matching items from the offset. No automatic pagination
occurs. Template lists also retain `details.default`.

Request `env` maps names to values. Response `env` is a list of names only.
Most timestamps are fractional Unix seconds. Terminal-ticket `expires_at` is an
RFC 3339 string. Optional response fields remain optional, and additional server
fields are preserved by the SDK models.

## Operations and lifecycle

Create/start/stop/resize/delete and network changes can enqueue work. Template
builds also return an operation ID. Poll the operation, rather than interpreting
the envelope's success message as completion. `operations.wait` returns the final
operation envelope on success and raises `SandboxOperationError` on failure.
Its `.operation` contains the last response. `SandboxOperationTimeoutError` holds
`.operation_id` and the last `.operation` if available. Timing out does not cancel
server work. HTTP errors propagate directly; polling requests disable internal
retries to keep polling deadlines bounded. Async waits are cancellable.

Stop/start preserves snapshots of memory, processes, and disk. Resize preserves
disk files but discards memory and running processes. `extend` adds its grant to
the current expiry. TTL continues during stop/start; lifecycle calls do not reset
it. Deletion or TTL expiry removes sandbox files.

## Safe retries and errors

Supported JSON mutations automatically get one idempotency key per invocation.
The same key is reused across internal retries. Pass `idempotency_key="..."` to
reuse a key across separate invocations of the **same** action. Keys must have
1–255 printable ASCII characters without spaces. The service retains them for
24 hours; changing the request while keeping a key returns a conflict. Retried
responses preserve operation IDs and can include `Idempotency-Replayed: true`.
Validation and execution failures may also be replayed; use a new key for a
corrected action. After `idempotency_result_unavailable`, inspect the resource
before deciding on a new action/key.

Streamed exec, binary uploads, and terminal tickets disable automatic retries.
The SDK rejects idempotency-key headers on these calls. A lost upload
acknowledgement can occur after commit; inspect the destination before retrying.
Do not set a global idempotency key when mixing these operations with JSON calls.

The existing `APIStatusError` hierarchy preserves `.body`, `.response`, and
`.status_code`, including gateway flat errors and service error envelopes.
For example, insufficient balance (402) remains an `APIStatusError`; a command
failure is reported in the successful exec result's `exit_code`.

## SSE exec

```python
stream = client.sandbox.sandboxes.exec_stream(
    krn_id=krn, x_region=region, cmd="echo hello; echo diagnostic >&2",
    timeout_seconds=600,
)
with stream:
    for event in stream:
        if event.type == "stdout":
            print(event.data, end="")
        elif event.type == "stderr":
            print(event.data, end="")
        elif event.type == "exit":
            print(event.exit_code, event.duration_ms)
```

Events preserve their `type`: `stdout`, `stderr`, or `exit`. Keepalive comments
are ignored. A server `error` event raises `SandboxStreamError` with a typed
`.event`; malformed events and disconnection before `exit` also raise it. Closing
the client stream does **not** kill the guest command. It can continue until its
execution timeout. The SDK never reconnects or re-executes a started stream.

For async, await `exec_stream`, then use `async with stream` and `async for`.
Use the stream context manager when breaking iteration early. Buffered exec
supports up to 120 seconds; streamed exec supports up to 3600. `timeout_seconds`
is the guest execution budget; the usual `timeout` option controls HTTP I/O.

## Files and response wrappers

Uploads send raw bytes, not multipart or base64. Use absolute guest paths whose
parent directories already exist. No implicit root elevation occurs. Sync
uploads accept `bytes` or an iterable of byte chunks; async uploads accept
`bytes` or an async iterable of byte chunks. No directory, archive, or resumable
transfer API is provided by this service.

```python
client.sandbox.files.upload(
    krn_id=krn, x_region=region, path="/tmp/input.bin", content=b"\x00\xff"
)
with client.sandbox.files.with_streaming_response.download(
    krn_id=krn, x_region=region, path="/tmp/input.bin"
) as response:
    response.stream_to_file("download.bin")
```

Ordinary `download` returns a `BinaryAPIResponse`; call `.read()` for bytes or
`.write_to_file(...)`. Async equivalents require `await`. Streaming wrappers
provide `.iter_bytes()` and `.stream_to_file(...)` and avoid buffering the entire
file. Interrupted downloads raise; any partial local file must be treated as
incomplete. Server errors before streaming use normal HTTP exceptions.

All HTTP methods offer both `resource.with_raw_response.method(...)` and
`client.with_raw_response.sandbox...method(...)`, exposing response headers and
`.parse()`. The matching `with_streaming_response` forms are context managers.
These wrappers do not apply to `operations.wait`.

## Background commands, networking, ports, and terminals

Background commands return immediately. Poll `commands.retrieve` using the
returned `stdout_offset` and `stderr_offset` to read new output. These are byte
offsets, not Python character counts. Status can become `exited`, `killed`,
`timed_out`, or `lost`; use `commands.kill` to terminate a running command.

`network.update` replaces the policy using PUT. Pass `network={}` to restore the
platform policy. Both retrieval and update return a `NetworkResponse` whose
`details` contains `egress`, `enforcement.status` (`pending`, `applied`, or
`failed`), and optional `enforcement.applied_at`. Updates also return
`details.operation_id`; pass that ID to `operations.wait` before depending on
enforcement. Domain
rules enforce DNS and subsequent connections; a wildcard does not cover the
bare domain. Private and other platform-blocked destinations remain restricted
by the server.

Token ports return a credential URL only from `ports.expose`. Store
`response.details.url` securely; lists cannot recover it. Private ports omit
that URL. `proxy_url` uses the owner's IAM authentication. Closing/re-exposing a
port changes its credentials. Access the URLs with an appropriate HTTP client;
the SDK does not add a generic proxy method.

`terminal.create_ticket` returns `details.url` and a one-use ticket valid for
60 seconds. Connect a WebSocket client directly to that returned URL. Query
options such as `cols`, `rows`, `cwd`, and `user` may be appended with URL query
encoding. No Authorization header is needed for the ticket URL. Keep the ticket
and its URL out of logs. The SDK does not manage WebSocket sessions.

For example, using an independently installed `websockets` package compatible
with your Python version:

```python
import json
import websockets

# Inside an async function, using AsyncKrutrimClient:
ticket = await client.sandbox.terminal.create_ticket(krn_id=krn, x_region=region)
async with websockets.connect(ticket.details.url) as ws:
    await ws.send(json.dumps({"type": "input", "data": "echo hello\n"}))
    async for frame in ws:
        event = json.loads(frame)
        if event["type"] == "exit":
            break
```

Frames include `ready`, `stdout`, `stderr`, `exit`, and `error`. Inputs can send
`input`, `resize`, `signal`, `close_stdin`, and `ping`. Closing a terminal
WebSocket ends its guest command, unlike disconnecting an SSE exec stream.

Runnable examples in `examples/sandbox_service` use `argparse`, have no import-time API
calls, and require an explicit gateway. No live smoke tests are run by the test
suite; its HTTP transports are mocked.
