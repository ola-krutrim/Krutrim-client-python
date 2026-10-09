# Custom Image Sandbox

Build a sandbox runtime with your own dependencies, publish it to a public
registry, and use it with `client.sandbox.create(image_uri=...)`.

This directory includes the [Dockerfile](Dockerfile), [Go module](agent/go.mod),
[runtime agent](agent/main.go), and [command parser](agent/shlex.go) needed to
build the image. No additional source repository is required.

## Prerequisites

- Docker with support for building `linux/amd64` images, plus curl.
- A public registry repository you can push to. The platform pulls anonymously;
  private images and images requiring pull credentials are not supported.
- Python 3.9 or newer, `krutrim-client`, and a Krutrim Cloud API key with sandbox
  access.

```bash
pip install krutrim-client
export KRUTRIMCLIENT_API_KEY="<your-api-key>"
export KRUTRIM_SANDBOX_REGION="In-Bangalore-1"
export KRUTRIM_SANDBOX_FLAVOR="sandbox-nano"
```

Choose a flavor available in your region. See the [basic recipe](../basic/)
for flavor discovery.

## 1. Use the Bundled Runtime Build Context

From this SDK repository's root:

```bash
cd examples/sandbox/cookbook/custom_image
```

This directory is the complete Docker build context:

```text
custom_image/
├── Dockerfile
├── README.md
├── main.py
└── agent/
    ├── go.mod
    ├── main.go
    ├── main_test.go
    └── shlex.go
```

The multi-stage Dockerfile builds a statically linked `sandbox-agent` with Go,
then copies it into an Ubuntu 24.04 runtime with Python, pip, venv, git, curl,
and network tools. Check the installed Python version rather than assuming
that the distribution's `python3` package is Python 3.13.

The runtime must keep the agent binary, its supported startup command, and its
HTTP contract intact:

| Endpoint | Purpose |
| --- | --- |
| `GET /` | Health check |
| `POST /execute` | Execute a command and return stdout, stderr, and exit code |
| `POST /upload` | Upload a file |
| `GET /download/{path}` | Download a file |
| `GET /list/{path}` | List a directory |
| `GET /exists/{path}` | Check whether a path exists |

An arbitrary Python or application image without this agent is not a sandbox
runtime image.

## 2. Add Your Dependencies

The bundled Dockerfile already installs `requests==2.32.5` for the SDK example.
To customize the dependencies, edit this step in its runtime stage, keeping it
**before** the `USER 1000` instruction:

```dockerfile
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir requests==2.32.5
ENV PATH="/opt/venv/bin:${PATH}"
```

Using a virtual environment avoids modifying Ubuntu's externally managed
system Python. Replace `requests` with your own pinned dependencies; use a
requirements file for larger dependency sets.

The baked-in `/opt/venv` is owned by root. For runtime package installs as a
non-root user, create a separate virtual environment under a writable directory
such as `/app` instead of modifying `/opt/venv`.

Add system packages to the existing `apt-get install` step, retaining
`--no-install-recommends` and the apt-list cleanup. Make application files
readable by UID 1000 and working directories writable by that user. Do not
bake API keys, registry credentials, or other secrets into a public image.

The image defaults to UID 1000 locally, but a deployment security context can
override the image user. Do not rely on `USER 1000` alone to enforce non-root
execution on the platform; verify the effective user for your deployment.

Keep `/usr/local/bin/sandbox-agent` and `CMD ["sandbox-agent"]`. The platform
template controls startup and health checks, so replacing the agent with your
application server will not work. Start application services separately on a
non-reserved port after sandbox creation.

## 3. Build for the Sandbox Platform

Replace `your-public-namespace` with your Docker Hub namespace, and create a
public repository named `custom-sandbox` there:

```bash
export KRUTRIM_SANDBOX_IMAGE="docker.io/your-public-namespace/custom-sandbox:v1"
docker build --platform linux/amd64 -t "$KRUTRIM_SANDBOX_IMAGE" .
```

The backend requires a `linux/amd64` manifest, a compressed image size no larger
than 4 GiB, and a registry that resolves only to public IPs. Use a versioned tag
so you can identify builds; the backend resolves and pins custom images to
their digest when creating a sandbox.

## 4. Smoke-Test Locally

Bind the unauthenticated runtime API to localhost only:

```bash
docker run -d --rm --name custom-sandbox-runtime \
  --platform linux/amd64 \
  -p 127.0.0.1:8871:8871 "$KRUTRIM_SANDBOX_IMAGE"

curl --fail-with-body http://127.0.0.1:8871/
curl --fail-with-body -X POST http://127.0.0.1:8871/execute \
  -H 'Content-Type: application/json' \
  -d '{"command":"python3 -c \"import requests; print(requests.__version__)\""}'
```

Expect health status `ok` and a command response with `exit_code: 0`, empty
stderr, and `2.32.5` in stdout if you added the dependency above. HTTP success
alone does not imply that the executed command succeeded: inspect `exit_code`.
The agent may take a moment to start; inspect `docker logs
custom-sandbox-runtime` if the initial health check cannot connect.

Exercise the file endpoints without creating a local test file:

```bash
printf 'hello from a custom image\n' | curl --fail-with-body \
  -X POST http://127.0.0.1:8871/upload \
  -F 'file=@-;filename=hello.txt'
curl --fail-with-body http://127.0.0.1:8871/list/.
curl --fail-with-body http://127.0.0.1:8871/download/hello.txt
curl --fail-with-body http://127.0.0.1:8871/exists/hello.txt
docker stop custom-sandbox-runtime
```

Expect the directory listing to include `hello.txt`, the download to return
the uploaded text, and the existence response to contain `exists: true`.

## 5. Publish and Check Anonymous Pull Access

Authenticate to your registry locally, then push:

```bash
docker login docker.io
docker push "$KRUTRIM_SANDBOX_IMAGE"
```

Check anonymous access with a temporary Docker configuration so your normal
registry login remains intact:

```bash
anonymous_config=$(mktemp -d)
DOCKER_CONFIG="$anonymous_config" docker pull \
  --platform linux/amd64 "$KRUTRIM_SANDBOX_IMAGE"
rm -r "$anonymous_config"
```

For GHCR or Quay, use the fully qualified image name and registry login for
that service instead. A successful authenticated push is not proof of public
pull access; ensure the repository or package visibility is public.

## 6. Create a Sandbox with the SDK

The runnable example is [main.py](main.py). From the SDK
repository root, run it with the API key, published image URI, region, and
flavor configured as above:

```bash
python examples/sandbox/cookbook/custom_image/main.py
```

The script requires the image built in step 2 with `requests` installed. It
prints the sandbox ID and resolved image, checks the Python and baked-in
`requests` versions, and uploads and reads back a message. For the image in
this recipe, output has this shape:

```text
Sandbox active: <sandbox-id>
Resolved image: <registry>/<namespace>/custom-sandbox@sha256:<digest>
Runtime and baked-in requests version:
<python-version-and-build>
2.32.5

File round-trip: hello from a custom image
```

The Docker build steps above run from the cookbook directory; return to the
SDK repository root with `cd ../../../..` before using the run command above.
Alternatively, run `python main.py` from this directory.

Missing configuration raises before creating a client. Command failures,
timeouts, and file mismatches raise an error; the context manager requests
sandbox deletion on success or failure. Running this example creates a real
sandbox and may incur charges.

Run this with the API key, image, region, and flavor environment variables
from the previous steps available in your Python process:

```python
import os

from krutrim_client import KrutrimClient

with KrutrimClient() as client:
    with client.sandbox.create(
        image_uri=os.environ["KRUTRIM_SANDBOX_IMAGE"],
        region=os.environ["KRUTRIM_SANDBOX_REGION"],
        flavor_name=os.environ["KRUTRIM_SANDBOX_FLAVOR"],
        timeout=900,
        wait_timeout=300,
    ) as sandbox:
        print("Sandbox active:", sandbox.sandbox_id)
        print("Resolved image:", sandbox.metadata.image_uri)
        sandbox.files.write("/app/message.txt", "hello from the SDK\n")
        result = sandbox.run_command(
            "python3 -c 'import requests; print(requests.__version__)'",
            cwd="/app",
            timeout=60,
        )
        if result.timed_out or result.exit_code != 0:
            raise RuntimeError(f"command failed: {result.stderr}")
        print(result.stdout)
        print(sandbox.files.read("/app/message.txt"))
```

This example assumes you baked in `requests` in step 2. Managed creation waits
for state `active`; `timeout=900` sets sandbox lifetime, while
`wait_timeout=300` limits readiness polling. Leaving the context manager
requests asynchronous deletion, including when the example raises.

The async client accepts the same `image_uri`:

```python
import asyncio
import os

from krutrim_client import AsyncKrutrimClient


async def main() -> None:
    async with AsyncKrutrimClient() as client:
        async with await client.sandbox.create(
            image_uri=os.environ["KRUTRIM_SANDBOX_IMAGE"],
            region=os.environ["KRUTRIM_SANDBOX_REGION"],
            flavor_name=os.environ["KRUTRIM_SANDBOX_FLAVOR"],
            timeout=900,
        ) as sandbox:
            result = await sandbox.run_command("python3 --version", timeout=60)
            if result.timed_out or result.exit_code != 0:
                raise RuntimeError(f"command failed: {result.stderr}")
            print(result.stdout)


asyncio.run(main())
```

Omit `image_uri` or pass `None` to use the platform runtime instead.

## Runtime Configuration and Troubleshooting

| Agent variable | Default | Purpose |
| --- | --- | --- |
| `SANDBOX_BASE_DIR` | `/app` | Working directory and boundary for agent file endpoints; must be writable |
| `SANDBOX_EXEC_TIMEOUT_SECONDS` | `300` | Agent's default command deadline; invalid values fall back to the default |
| `PORT` | `8871` | Runtime HTTP port; the platform template sets this |

Template environment variables override user-supplied values, including
`PORT`. Do not expose the reserved agent port as a user port or publish the
local agent directly to the Internet: it permits command execution without
authentication. Use the SDK's authenticated API and proxy for hosted access.

- **Build fails:** run Docker from this cookbook directory so it can find the
  bundled `agent/` files. Keep the source files together rather than mixing
  snippets from different revisions.
- **HTTP 400 during creation:** check public pull access, architecture, image
  size, and registry address restrictions. The SDK raises `BadRequestError`.
- **Creation accepted but startup fails:** check the agent binary, startup
  command, health endpoint, port, and UID 1000 permissions. Managed creation
  raises `SandboxException` with backend diagnostics and last known metadata.
- **Readiness deadline exceeded:** managed creation raises
  `SandboxTimeoutError`. Inspect backend diagnostics and image startup before
  increasing `wait_timeout`; avoid blindly retrying creation.
- **Shell operators do not work in direct `/execute` requests:** the agent
  parses arguments without a shell. Invoke one explicitly, for example
  `bash -c 'ls | wc -l'`.
- **Pip refuses a runtime install:** use a writable virtual environment rather
  than the distribution's system Python, or bake dependencies into the image.

See the [Sandbox guide](../../../../docs/sandbox.md#bring-your-own-container-byoc)
for BYOC constraints and timeout semantics, the [SDK
reference](../../../../docs/sandbox-sdk-reference.md) for parameter details,
and the [ports and proxy recipe](../web_service_ports_proxy/) to run an
application service alongside the agent.