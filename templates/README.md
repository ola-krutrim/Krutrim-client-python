# Krutrim Sandbox templates

Container images for the Sandbox BYOC path (`create_sandbox(image_uri=...)`).

Published by `.github/workflows/publish-templates.yml` on a `template-v*` tag, to
`ghcr.io/ola-krutrim/sandbox-<template>`.

## Templates

20 templates, all published as `ghcr.io/ola-krutrim/sandbox-<name>`.

| template | contents |
|---|---|
| `aider` | Aider pair-programming agent |
| `browser-playwright` | Playwright with Chromium, Firefox and WebKit |
| `bun` | Bun runtime and package manager |
| `claude-code` | Anthropic Claude Code CLI |
| `code-interpreter` | Python data stack and Jupyter kernel |
| `codex` | OpenAI Codex CLI |
| `computer-use` | Xvfb and a real Chromium for browser-driving agents |
| `data-science` | scikit-learn, scipy, polars, duckdb |
| `database` | PostgreSQL, SQLite and Redis |
| `deno` | Deno runtime |
| `documents` | Pandoc and LaTeX for PDF and document conversion |
| `ffmpeg` | ffmpeg and image tooling |
| `golang` | Go toolchain |
| `java` | Temurin JDK 21, Maven, Gradle |
| `nodejs` | Node 22 LTS with pnpm and yarn |
| `opencode` | OpenCode agent CLI |
| `php` | PHP CLI with Composer |
| `ruby` | Ruby with bundler |
| `rust` | Rust toolchain via rustup |
| `terminal-bench` | tmux, asciinema and terminal tooling |

Pin by digest in production. The current computer-use digest, for example:

```
ghcr.io/ola-krutrim/sandbox-computer-use@sha256:535d7441746008113b3427a76f6ec24a6152d2746272edc9475957a9eafe9211
```

## The base image

Every template builds `FROM ghcr.io/ola-krutrim/sandbox-base`. The base carries the
BYOC contract — the `sandbox-agent` binary, port 8871, `/app` owned by UID 1000 — and a
template adds only its own tools.

This is worth keeping. Shared base layers dedupe in the registry rather than being
stored twenty times, the base is cached on the node after the first pull so each
additional template costs little beyond its own layer, and a CVE in the base is patched
in one Dockerfile instead of twenty.

The build is two-phase: `sandbox-base` first, then every template against it, pinned
with `BASE_TAG` so a tagged release is reproducible.

## These images must be public

The platform pulls **anonymously** — private registries and pull credentials are not
supported. A private package cannot be used at all. The publish workflow verifies the
anonymous pull path explicitly (logging out of GHCR first), because an authenticated
test would pass while the real path fails.

Note that `ola-krutrim` disallows public packages at the organisation level by default.
Publishing a usable template requires that policy to permit public packages, and the
visibility of each package is then set once by hand — GitHub exposes no REST endpoint
for it, so the workflow's attempt is best-effort and expected to fail quietly.

## What a template costs at create time

Measured on `sandbox-large` in In-Bangalore-1, create → usable, with stock-image
controls taken in the same run:

| | time |
|---|---|
| stock image (3 creates) | 1.56 / 1.46 / 1.42 s |
| this template, warm (4 creates) | 2.15 / 2.17 / 2.12 / 2.14 s |
| **steady-state penalty** | **+0.68 s median** |
| first create of a new image in a region | 40.13 s, once |
| second create | 16.19 s |

**Images are cached.** Only the first pull into a region is expensive; after that a
521 MiB image costs under a second against a 1.46 s baseline. Do not size a template
budget from a cold create — that number is a one-time warming cost, not the price of
using a template.

Cache scope is not documented and was not determined here: four consecutive fast
creates are consistent with a warm cache, but whether it is per node, per zone or per
region is unverified, and all four may have landed on one node.

## Contract each template must satisfy

| requirement | value |
|---|---|
| platform | `linux/amd64` |
| user | non-root, UID 1000 — but see the note below |
| workdir | `/app`, owned by 1000 |
| agent | bundles `sandbox-agent`, entrypoint starts it |
| port | 8871 (or 8888) |
| routes | `GET /`, `POST /execute`, `/download/{path}`, `/list/{path}`, `/exists/{path}` |
| size | <= 4 GiB compressed |
| registry | public, anonymous pull, resolves to public IPs |

### The UID 1000 requirement is not enforced at runtime

Build for it anyway — it is what the contract asks for, and that may change. But be
aware of what actually happens. This image declares `USER 1000` and `docker inspect`
confirms it, yet inside a running sandbox:

```
uid=0(root) gid=0(root) groups=0(root)
PID 1 = sandbox-agent        /proc/1/status  Uid: 0 0 0 0
/app  owner uid 1000, mode 755
```

Stock sandboxes also run as uid 0, so this is consistent rather than BYOC-specific.
**Do not treat "runs as UID 1000" as a security property of your workload.** gVisor is
the actual isolation boundary. Tracked in the Omni tracker.

## computer-use

Xvfb plus a real Chromium, so agents can drive a browser inside a sandbox.

Ubuntu's apt `chromium-browser` is a **snap shim** and cannot work in a container — it
only prints *"requires the chromium snap to be installed"*, and snap needs systemd,
which is not present. Xvfb itself runs fine. This image installs Playwright's bundled
Chromium, which is a real binary.

From the published image, with no runtime installation:

```
with-display <chromium> --headless=new --dump-dom https://example.com
  -> <title>Example Domain</title>    in 2.9 s
```

Reaching the same state by installing at runtime costs roughly **100 s and 310 MB on
every create**. That is the entire argument for baking a template, and it is why the
cookbook's advice to *"avoid installing large packages during sandbox initialization"*
is not followable without one.

Contents:

```
/usr/local/bin/sandbox-agent                          built from the cookbook agent
/opt/playwright/chromium-1248/chrome-linux64/chrome   real Chromium binary
/usr/local/bin/with-display                           starts Xvfb :99, then execs
```

Size: 521 MiB compressed, 1.97 GB uncompressed, 9 layers.

## Build context

These images build from the **repository root**, not from their own directory, so the
Dockerfile can `COPY` the agent straight out of
`examples/sandbox/cookbook/custom_image/agent`. There is deliberately no second copy of
the agent source under `templates/` — that agent implements the sandbox contract, and a
duplicate would drift out of sync without anyone noticing.

## Adding a template

1. Add `templates/<name>/Dockerfile`, building from the repository root.
2. Add `<name>` to the build matrix in `.github/workflows/publish-templates.yml`.
3. Tag `template-v*` and push. The workflow builds, pushes, checks the 4 GiB limit and
   verifies the anonymous pull.
4. Set the new package's visibility to public once, by hand.
