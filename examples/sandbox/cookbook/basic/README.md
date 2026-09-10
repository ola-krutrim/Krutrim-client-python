# Omni Sandbox Examples

These examples create an isolated sandbox, upload a small Python program, run it, and read the result back.

| Example | Client |
| --- | --- |
| `RunSandbox.py` | Synchronous `KrutrimClient` |
| `RunSandboxAsync.py` | Asynchronous `AsyncKrutrimClient` |

## Prerequisites

1. Install the SDK:

   ```bash
   pip install krutrim-client
   ```

2. Set your API key:

   ```bash
   export KRUTRIMCLIENT_API_KEY="<your-api-key>"
   ```

3. Choose a region and flavor. You can list the flavors available in a region:

   ```python
   from krutrim_client import KrutrimClient

   with KrutrimClient() as client:
       for flavor in client.sandbox.api.list_flavors(region="In-Bangalore-1").data or []:
           group = flavor.group_by
           print(flavor.name or (group.flavorname if group else None))
   ```

## Run

```bash
export KRUTRIM_SANDBOX_REGION="In-Bangalore-1"
export KRUTRIM_SANDBOX_FLAVOR="sandbox-large"

python RunSandbox.py        # synchronous client
python RunSandboxAsync.py   # asynchronous client
```

Expected output:

```
Sandbox active: <sandbox-id>
Agent result:
{
  "result": 42
}
```

## What the examples do

1. `client.sandbox.create(...)` creates the sandbox and waits until it is `active` (`timeout=900` sets the sandbox lifetime in seconds).
2. `sandbox.files.make_dir` / `sandbox.files.write` upload a program and its JSON input.
3. `sandbox.run_command` executes the program; the result reports `exit_code`, `stdout`, `stderr`, and `timed_out` instead of raising on program failure.
4. `sandbox.files.read` downloads the output file.
5. Leaving the `with` block requests sandbox deletion automatically.

See [docs/sandbox.md](../../docs/sandbox.md) for the full sandbox guide, including low-level API access, timeout semantics, ports, and proxying.
