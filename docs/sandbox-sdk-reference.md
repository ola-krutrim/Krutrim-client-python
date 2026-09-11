# Omni Sandbox SDK Reference

Reference for the sandbox functions you call as an SDK user. For a narrative introduction see
the [Omni Sandbox guide](sandbox.md); for agent-oriented usage see the
[agent guide](sandbox-agent-guide.md).

> **Note.** The SDK also exposes `client.sandbox.api`, a low-level 1:1 mirror of the REST
> contract (raw response envelopes, no readiness polling, raw/streaming views). It is an
> escape hatch for advanced integrations and is covered in the [guide](sandbox.md), not here.
> Everyday code should use the managed functions below.

## Getting started

```python
from krutrim_client import KrutrimClient

client = KrutrimClient()  # api_key from KRUTRIMCLIENT_API_KEY

with client.sandbox.create(
    flavor_name="sandbox-nano",
    region="In-Bangalore-1",
    timeout=900,                    # sandbox lifetime in seconds
) as sandbox:
    sandbox.files.write("/app/hello.py", 'print("hello")')
    result = sandbox.run_command("python3 hello.py", cwd="/app")
    print(result.stdout)
# leaving the block deletes the sandbox
```

Every function has an identical async variant on `AsyncKrutrimClient` — `await` each call and
use `async with await client.sandbox.create(...) as sandbox:`.

## Function index

| Function | Returns | Purpose |
| --- | --- | --- |
| `client.sandbox.create(...)` | `Sandbox` | Create a sandbox |
| `client.sandbox.connect(sandbox_id)` | `Sandbox` | Attach to an existing sandbox |
| `sandbox.run_command(command, ...)` | `SandboxCommandResult` | Execute a shell command |
| `sandbox.set_timeout(seconds)` | `None` | Reset the sandbox lifetime |
| `sandbox.is_running()` | `bool` | Check whether the sandbox is active |
| `sandbox.kill()` | `None` | Delete the sandbox |
| `sandbox.files.write(path, data)` | `SandboxFileData` | Upload a file |
| `sandbox.files.read(path)` | `str \| bytes` | Download a file |
| `sandbox.files.remove(path)` | `SandboxFileData` | Delete a file or directory |
| `sandbox.files.list(path, depth)` | `List[SandboxEntryInfo]` | List directory entries |
| `sandbox.files.stat(path)` | `SandboxEntryInfo` | Get metadata for one entry |
| `sandbox.files.rename(path, new_path)` | `SandboxFileData` | Move or rename an entry |
| `sandbox.files.make_dir(path)` | `SandboxFileData` | Create a directory |
| `sandbox.ports.open(port)` | `SandboxPortInfo` | Expose a port |
| `sandbox.ports.list()` | `List[SandboxPortInfo]` | List exposed ports |
| `sandbox.ports.close(port)` | `None` | Close an exposed port |
| `sandbox.proxy.request(method, path, ...)` | `bytes` | Send an HTTP request into the sandbox |
| `client.sandbox.api.list_flavors(region=...)` | `FlavorListResponse` | Discover compute flavors |
| `client.sandbox.api.list_templates()` | `List[PodTemplate]` | Discover runtime templates |
| `client.sandbox.api.list(...)` | `SandboxListResponse` | List your sandboxes |

---

## Discovery

These three calls live on `client.sandbox.api` because they have no managed wrapper, but they
are part of the normal user workflow: use them to find valid `flavor_name`, `template_name`,
and existing sandbox IDs before calling `create`/`connect`.

### `client.sandbox.api.list_flavors(*, region=None) -> FlavorListResponse`

Lists compute flavors, optionally filtered by region. Iterate `response.data` (`FlavorItem`
objects with `id`, `name`, `resources`).

### `client.sandbox.api.list_templates() -> List[PodTemplate]`

Lists runtime templates. Use a template's `template_name` (or `id`) with `create`.

### `client.sandbox.api.list(*, region=None, status=None, name=None, page=None, limit=None) -> SandboxListResponse`

Paginated listing of your sandboxes (`page >= 1`, `limit` 1–100). Rows are in
`response.data.rows`; each row's `id` can be passed to `connect`.

---

## Lifecycle — `client.sandbox`

### `create(...) -> Sandbox`

Creates a sandbox, waits until its status is `active`, and returns a ready-to-use handle.

```python
def create(
    *,
    flavor_name: str,                                   # required, e.g. "sandbox-nano"
    region: str,                                        # required, e.g. "In-Bangalore-1"
    sandbox_name: str | None = None,                    # auto-generated "sandbox-<12 hex>" if omitted
    template_id: int | None = None,                     # mutually exclusive with template_name
    template_name: str | None = None,
    network_storages: Sequence[NetworkStorageAttachmentInput] | None = None,  # max 10
    environment_variables: Mapping[str, str] | None = None,
    timeout: int | None = None,                         # sandbox lifetime in seconds (60–604800)
    wait_timeout: float = 300.0,                        # total readiness deadline (> 0)
    request_timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,  # per-HTTP-call
) -> Sandbox
```

Behavior:

- `sandbox_name` must be DNS-1035 (lowercase letters, digits, hyphens; starts with a letter).
- Polls readiness with exponential backoff (0.25 s doubling, capped at 2 s); transient
  `404`s right after creation are tolerated until the sandbox first becomes visible.
- Raises `SandboxException` if deployment fails (`failed_deploy`), the sandbox starts
  deleting, or it disappears after being seen.
- Raises `SandboxTimeoutError` when `wait_timeout` elapses before the sandbox is `active`.
- Raises `ValueError` for invalid names, lifetimes, or `template_id`+`template_name` together.

### `connect(sandbox_id, *, wait_timeout=300.0, request_timeout=NOT_GIVEN) -> Sandbox`

Attaches to an existing sandbox and waits until it is `active`. A `404` is an immediate
`SandboxException` (no tolerance window, since nothing was just created).

---

## Sandbox handle — `Sandbox`

Returned by `create`/`connect`; every method targets the bound sandbox.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `sandbox_id` | `str` | Sandbox identifier. |
| `sandbox_krn` | `str \| None` | Krutrim resource name. |
| `metadata` | `SandboxResponse` | Last fetched metadata (refreshed by `is_running`). |
| `files` / `commands` / `ports` / `proxy` | helpers | Documented below. |

### `run_command(command, *, cwd=None, envs=None, timeout=60, request_timeout=NOT_GIVEN) -> SandboxCommandResult`

Executes a shell command inside the sandbox (alias for `sandbox.commands.run`).

| Parameter | Constraint |
| --- | --- |
| `command` | 1–100,000 characters |
| `cwd` | optional working directory |
| `envs` | optional `Mapping[str, str]` of environment variables |
| `timeout` | execution deadline in the sandbox, 1–270 seconds |
| `request_timeout` | HTTP timeout; defaults to `timeout + 30` s so the transport doesn't expire first |

Program failure is **data, not an exception** — inspect the result:

```python
result = sandbox.run_command("python3 program.py", cwd="/app/work", timeout=120)
if result.exit_code != 0 or result.timed_out:
    raise RuntimeError(result.stderr)
```

### `set_timeout(timeout, *, request_timeout=NOT_GIVEN) -> None`

Resets the sandbox lifetime to *now + `timeout` seconds* (not additive). Range 60–604,800.

### `is_running(*, request_timeout=NOT_GIVEN) -> bool`

Returns `True` only when the sandbox status is `active`; `False` if it no longer exists.
Also refreshes `sandbox.metadata`.

### `kill(*, request_timeout=NOT_GIVEN) -> None`

Requests sandbox deletion. Idempotent — repeated calls and already-deleted sandboxes are
no-ops. Deletion is asynchronous server-side: acceptance is guaranteed, cluster cleanup is not.

### Context manager

`with client.sandbox.create(...) as sandbox:` calls `kill()` on exit — including when the body
raises. If the body raised and cleanup also fails, the body exception stays primary and the
cleanup failure is attached as diagnostic information.

---

## Filesystem — `sandbox.files`

Paths are absolute paths inside the sandbox. Uploads are capped at 100 MB.

### `write(path, data) -> SandboxFileData`

Uploads a file. `data` may be a `str` (encoded UTF-8), `bytes`, a binary file object, or a
local `os.PathLike` to read from disk. Other types raise `TypeError`; > 100 MB raises
`ValueError`.

### `read(path, *, format="text") -> str | bytes`

Downloads a file. `format="text"` (default) decodes UTF-8 (propagating `UnicodeDecodeError`);
`format="bytes"` returns exact bytes. Any other value raises `ValueError`.

### `remove(path) -> SandboxFileData`

Deletes the file or directory at `path`.

### `list(path=None, *, depth=None) -> List[SandboxEntryInfo]`

Lists directory entries. `depth` (1–10) controls recursion. Returns `[]` for empty results.

### `stat(path=None) -> SandboxEntryInfo`

Returns metadata for one entry: `name`, `path`, `type` (`"file"`/`"dir"`), `size`, `mode`,
`modified_time`.

### `rename(path, new_path) -> SandboxFileData`

Moves/renames an entry. Both paths must be non-empty.

### `make_dir(path) -> SandboxFileData`

Creates a directory.

```python
sandbox.files.make_dir("/app/work")
sandbox.files.write("/app/work/input.json", '{"value": 21}')
entries = sandbox.files.list("/app/work", depth=2)
text = sandbox.files.read("/app/work/input.json")
blob = sandbox.files.read("/app/work/input.json", format="bytes")
sandbox.files.rename("/app/work/input.json", "/app/work/in.json")
sandbox.files.remove("/app/work/in.json")
```

---

## Ports — `sandbox.ports`

Valid range 1024–65535; the service allows at most 20 open ports per sandbox.

### `open(port) -> SandboxPortInfo`

Requests public exposure of a port. The returned port may already be `active` or still
`provisioning` — the SDK does not poll, so call `list()` until the port reports
`status == "active"`, then use its `url`. The `url` may be gateway-relative; join it with
the client's base URL before sharing.

### `list() -> List[SandboxPortInfo]`

Returns all ports with `port`, `status` (`provisioning`/`active`/`closing`/`failed`),
`error_message`, and `url`.

### `close(port) -> None`

Closes an exposed port.

```python
sandbox.ports.open(8000)
while not any(p.port == 8000 and p.status == "active" for p in sandbox.ports.list()):
    time.sleep(1)
```

---

## Proxy — `sandbox.proxy`

### `request(method, path, *, query=None, headers=None, json=None, content=None, max_retries=0, request_timeout=NOT_GIVEN) -> bytes`

Sends an HTTP request to a service running inside the sandbox and returns the exact response
body bytes.

- `method`: `GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS` (case-insensitive); others raise
  `ValueError`.
- `path`: `/port/{port}/<service-path>`, where `{port}` is a port previously opened via
  `sandbox.ports` and currently `active`; `..` traversal segments raise `ValueError`.
- `json` and `content` are mutually exclusive; `content` (str/bytes) is capped at 100 MB.
- `max_retries` defaults to `0` so non-idempotent requests are never silently repeated.
- HTTP errors raise the SDK's normal `APIStatusError` subclasses; a path that does not use
  an active port's `/port/{port}/` prefix fails with `NotFoundError`.

```python
sandbox.ports.open(8000)
while not any(p.port == 8000 and p.status == "active" for p in sandbox.ports.list()):
    time.sleep(1)
body = sandbox.proxy.request("POST", "/port/8000/api/v1/predict", json={"x": 1})
```

---

## Result models

Returned by the functions above (importable from `krutrim_client.types.sandbox`):

| Model | Fields |
| --- | --- |
| `SandboxCommandResult` | `stdout`, `stderr`, `exit_code`, `stdout_truncated`, `stderr_truncated`, `timed_out` |
| `SandboxEntryInfo` | `name`, `path`, `type` (`file`/`dir`), `size`, `mode`, `modified_time` |
| `SandboxFileData` | `path`, `name`, `type` |
| `SandboxPortInfo` | `port`, `status` (`provisioning`/`active`/`closing`/`failed`), `error_message`, `url` |
| `SandboxResponse` (`sandbox.metadata`) | `id`, `name`, `krn`, `status`, `region`, `service_url`, `flavor_name`, `ttl_seconds`, `expires_at`, `created_at`, resource sizes, … |
| `PodTemplate` | `id`, `template_name`, `description`, image/disk/port settings |
| `FlavorItem` | `id`, `name`, `resources` |

## Exceptions

| Exception | Raised when |
| --- | --- |
| `SandboxException` | Sandbox failed to deploy, disappeared, or returned an incomplete response. Carries `sandbox_id` and `metadata`. |
| `SandboxTimeoutError` | `wait_timeout` elapsed before the sandbox became active (subclass of `SandboxException`). |
| `ValueError` / `TypeError` | Client-side validation failures (limits below, unsupported content types). |
| `NotFoundError`, `ConflictError`, `APITimeoutError`, other `APIStatusError` subclasses | Standard SDK HTTP errors. |

## Limits

| Constraint | Range / rule |
| --- | --- |
| Sandbox lifetime (`timeout` / `set_timeout`) | 60–604,800 seconds |
| `sandbox_name` | DNS-1035 lowercase name |
| `wait_timeout` | > 0 seconds (default 300) |
| Command length | 1–100,000 characters |
| Command timeout | 1–270 seconds (default 60) |
| Ports | 1024–65535; max 20 open per sandbox |
| File / proxy body size | ≤ 100 MB |
| Directory listing `depth` | 1–10 |
| `template_id` / `template_name` | mutually exclusive |
| `network_storages` | at most 10 attachments |
