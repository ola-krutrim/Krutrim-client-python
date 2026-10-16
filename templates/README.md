# Krutrim Sandbox templates

Container images for the Sandbox BYOC path (`create_sandbox(image_uri=...)`).

Published by `.github/workflows/publish-templates.yml` on a `template-v*` tag, to
`ghcr.io/ola-krutrim/sandbox-<template>`.

## These images must be public

The platform pulls **anonymously** — private registries and pull credentials are not
supported. A private package cannot be used at all. The publish workflow therefore
sets package visibility to public and verifies the anonymous pull path explicitly
(logging out of GHCR first), because an authenticated test would pass while the real
path fails.

## Contract each template must satisfy

| requirement | value |
|---|---|
| platform | `linux/amd64` |
| user | non-root, UID 1000 |
| workdir | `/app`, owned by 1000 |
| agent | bundles `sandbox-agent`, entrypoint starts it |
| port | 8871 (or 8888) |
| routes | `GET /`, `POST /execute`, `/download/{path}`, `/list/{path}`, `/exists/{path}` |
| size | <= 4 GiB compressed |
| registry | public, anonymous pull, resolves to public IPs |

## computer-use

Xvfb plus a real Chromium, so agents can drive a browser inside a sandbox.

Note that Ubuntu's apt `chromium-browser` is a **snap shim** and cannot work in a
container — it only prints *"requires the chromium snap to be installed"*. This image
installs Playwright's bundled Chromium, which is a real binary. Doing this at runtime
instead costs roughly 100 s and 310 MB on every create; that is what baking removes.

Verified on a native amd64 build, 2026-10-16:

```
User=1000  WorkingDir=/app  Cmd=[sandbox-agent]  Exposed=8871/tcp  Arch=amd64/linux
/usr/local/bin/sandbox-agent                          6029496 bytes
/opt/playwright/chromium-1248/chrome-linux64/chrome   real binary
1.97 GB uncompressed
```

## Build context

These images build from the **repository root**, not from their own directory, so the
Dockerfile can `COPY` the agent straight out of
`examples/sandbox/cookbook/custom_image/agent`. There is deliberately no second copy of
the agent source under `templates/` — that agent implements the sandbox contract, and a
duplicate would drift out of sync without anyone noticing.
