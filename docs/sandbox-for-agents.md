# Sandbox for agents

A task-oriented guide for an AI agent driving Krutrim Sandbox. `llms.txt` at the
repository root is the compressed version; this is the same material with the reasoning
and the failure modes attached.

Measured against production in In-Bangalore-1 on 2026-10-17 at `template-v1.2.1`.

## When to reach for a sandbox

- **Running code you did not write** — model-generated scripts, an unaudited dependency,
  a user's reproduction. It executes behind a gVisor syscall boundary on a machine that
  is not the host, and it is destroyed afterwards.
- **You need a different architecture or OS** — amd64 Linux from an arm64 machine, in
  about two seconds, with no local container runtime.
- **A toolchain you do not have** — 21 templates ship Go, Rust, Java, Node, Bun, Deno,
  Ruby, PHP, a data stack, databases, browsers, document and media tooling, and five
  coding-agent CLIs.
- **Work that should not touch the host filesystem or network identity.**

Do not reach for one for a long-lived service. The TTL caps at seven days and the design
point is disposability.

## The loop

```python
from krutrim_client import KrutrimClient

c = KrutrimClient()                      # reads KRUTRIMCLIENT_API_KEY

with c.sandbox.create(
    sandbox_name="task-run",
    region="In-Bangalore-1",
    flavor_name="sandbox-small",
    timeout=900,
    image_uri="ghcr.io/ola-krutrim/sandbox-code-interpreter:template-v1.2.1",
) as sb:
    sb.files.write("/app/job.py", source)
    out = sb.run_command("python3 /app/job.py", timeout=240)
    if out.exit_code != 0:
        raise RuntimeError(out.stderr)
    result = sb.files.read("/app/out.json")
```

Three things in that example are not decoration:

1. **The context manager destroys the sandbox**, including on an exception. A sandbox
   bills until destroyed or reaped.
2. **Paths are under `/app`.** The files API is rooted at `SANDBOX_BASE_DIR`, and a path
   outside it is silently rebased while the response reports the path you passed.
3. **`timeout` on `run_command` must be <= 270.** It is a client-side limit, so it raises
   immediately rather than at the deadline.

## Generating sandbox names

The service rejects a name longer than 28 characters with an HTTP 400. Agents generate
names from a prefix, a run id and a task name, which crosses 28 easily, and in a loop the
failure reads as "this one task is broken" rather than "this name is long".

```python
import re, uuid

def sandbox_name(prefix: str, limit: int = 28) -> str:
    suffix = "-" + uuid.uuid4().hex[:6]
    stem = prefix.lower()[: limit - len(suffix)].strip("-")   # truncate THEN strip
    if not stem or not stem[0].isalpha():
        stem = "sb" + stem
    return stem + suffix
```

Truncating after stripping is not equivalent: `"browser-playwright"[:8]` is `"browser-"`,
and DNS-1035 requires an alphanumeric final character.

## Work longer than 270 seconds

Launch it detached inside the sandbox and poll a marker file. Write the exit code as the
last action so the marker's existence means completion.

```python
sb.files.write("/app/job.sh", script)          # script ends: echo $? > /app/job.rc
sb.run_command(
    "rm -f /app/job.rc && setsid nohup bash /app/job.sh "
    "> /app/job.log 2>&1 < /dev/null & sleep 1; echo launched", timeout=60)

while time.time() < deadline:
    time.sleep(10)
    probe = sb.run_command(
        "[ -f /app/job.rc ] && echo DONE rc=$(cat /app/job.rc) || echo RUNNING", timeout=60)
    if probe.stdout.strip().startswith("DONE"):
        break
```

Capture the exit code into a variable before echoing it. `cmd; echo "x=$?"; echo $? > rc`
records the `echo`'s status, not the command's.

## Running many sandboxes

Space creates by about 8 seconds. Unspaced bursts degrade from ~2 s to 12-42 s and then
fail — one failure arrives as a raw `403 Forbidden` HTML page which the SDK raises as
`PermissionDeniedError`. It is a rate limit wearing a credentials error, and because it is
a 403 rather than a 429 with `Retry-After`, a conventional retry policy will not retry it.
An agent that treats `PermissionDeniedError` as an auth failure will stop and report a
credentials problem that does not exist.

## Reading results back

A sandbox dies with everything inside it. Read artifacts out before the block exits, or
attach network storage. `files.read` returns text by default and accepts
`format="bytes"`.

## What is not enforced

- **Egress policy.** `allow_internet_access` and the allowlist parameters are accepted,
  echoed back with HTTP 200, and do nothing. They fail **open**. If an agent's safety
  argument depends on restricting a sandbox's network access, that argument does not
  currently hold.
- **The image's `USER`.** Containers start as uid 0 regardless.
- **Outbound identity.** Every sandbox in a region shares one NAT address, so request
  volume against a third party is a shared budget, not a private one.

## Cost

A full repository clone-and-build is about Rs 0.09; a browser page fetch about Rs 0.01.
A template adds roughly 0.8 s over a bare sandbox and that does not grow with image size.
The first pull of an image into a region costs 8-71 s once, which is not the steady-state
price and should not be used for budgeting or timeouts.

## Verifying a template rather than trusting it

A version string is not a working toolchain. `template-v1.2.0` shipped a `rust` image
where `rustc --version` was correct and `cargo build` failed with ``linker `cc` not
found``, because rustup installs a compiler and not a C toolchain. Every CI job was green.

If an agent depends on a template, exercise the capability — compile something, execute
something, query something — rather than asking for a version. The publish workflow now
does this per template, but the habit is worth keeping.

## See also

- `llms.txt` — the compressed, self-contained version of this file
- `docs/sandbox-sdk-reference.md` — every call, parameter and limit
- `templates/` — Dockerfiles, digests and the measured capability table
- `examples/sandbox/cookbook/custom_image/` — building your own image against the contract
