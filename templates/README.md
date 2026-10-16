# Krutrim Sandbox templates

Container images for the Sandbox BYOC path (`create_sandbox(image_uri=...)`).

Published by `.github/workflows/publish-templates.yml` on a `template-v*` tag, to
`ghcr.io/ola-krutrim/sandbox-<template>`.

## Templates

21 templates, all published as `ghcr.io/ola-krutrim/sandbox-<name>`.

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
| `hermes` | Hermes Agent, the Nous Research open-source agent |
| `java` | Temurin JDK 21, Maven, Gradle |
| `nodejs` | Node 22 LTS with pnpm and yarn |
| `opencode` | OpenCode agent CLI |
| `php` | PHP CLI with Composer |
| `ruby` | Ruby with bundler |
| `rust` | Rust toolchain via rustup |
| `terminal-bench` | tmux, asciinema and terminal tooling |

## Using a template

Templates are consumed through the BYOC path: `create` takes an `image_uri`. There is no
`template_name` parameter — the `/omni/sandbox/v1/template` catalog is read-only in SDK
0.8.4 — so a published image reference is the whole interface.

```python
from krutrim_client import KrutrimClient

c = KrutrimClient(api_key="...")

r = c.sandbox.api.create(
    sandbox_name="my-agent",          # DNS-1035, and 28 characters or fewer
    region="In-Bangalore-1",
    flavor_name="sandbox-large",
    ttl_seconds=900,
    image_uri="ghcr.io/ola-krutrim/sandbox-hermes:template-v1.1.0",
)

sb = c.sandbox.connect(r.data.id)
print(sb.run_command("hermes --version").stdout)

c.sandbox.api.delete(r.data.id)
```

`sandbox_name` must be **28 characters or fewer**. The SDK validates the DNS-1035 shape
but not the length, so an over-long name comes back as a server-side 400 rather than a
local `ValueError` — easy to hit when a name is built from a template name and a run id.

Nothing needs credentials to pull. The platform fetches these anonymously, which is why
each one is published public and the release workflow proves that path with GHCR logged
out.

## What each template proves, measured

Every row below was created from the published `template-v1.1.0` image in
In-Bangalore-1 on `sandbox-large`, and the listed tool was run inside the sandbox.
21 of 21 passed.

| template | MiB compressed | create → usable (s) | verified in a live sandbox |
|---|---|---|---|
| `aider` | 233 | 28.0 | `aider 0.86.2` |
| `browser-playwright` | 950 | 65.4 | Chromium, Firefox and WebKit all launched a page |
| `bun` | 124 | 11.8 | `bun 1.4.3` |
| `claude-code` | 371 | 37.5 | `2.1.301 (Claude Code)` |
| `code-interpreter` | 173 | 18.3 | `pandas 3.0.6`, kernel registered |
| `codex` | 453 | 44.4 | `codex-cli 0.163.0` |
| `computer-use` | 522 | 43.7 | `with-display` shim, `chromium-1248` |
| `data-science` | 386 | 39.7 | `sklearn 1.9.1`, polars, duckdb, pyarrow |
| `database` | 182 | 17.9 | PostgreSQL 16.15, SQLite 3.45.1, Redis 7.0.15 |
| `deno` | 124 | 9.5 | `deno 2.9.7` |
| `documents` | 312 | 30.9 | `pandoc 3.1.3`, pypdf/docx/openpyxl |
| `ffmpeg` | 302 | 26.8 | `ffmpeg 6.1.1`, Pillow, imageio |
| `golang` | 158 | 15.9 | `go1.24.8 linux/amd64` |
| `hermes` | 140 | 13.9 | `Hermes Agent v0.19.0` |
| `java` | 327 | 30.9 | `openjdk 21.0.12.1`, Maven 3.8.7 |
| `nodejs` | 192 | 18.4 | `node v22.23.3`, pnpm 12.11.2, yarn 1.22.22 |
| `opencode` | 408 | 41.4 | `1.19.2` |
| `php` | 105 | 10.1 | `PHP 8.3.6`, Composer |
| `ruby` | 181 | 20.1 | `ruby 3.2.3`, bundler 4.0.23 |
| `rust` | 294 | 28.8 | `rustc 1.99.1`, cargo 1.99.1 |
| `terminal-bench` | 93 | 5.4 | tmux 3.4, asciinema 2.4.0, ripgrep 14.1.0 |

Those create times are each a **first-ever pull of that image into the region**; the
median is 26.8 s. Once an image is cached in a region the steady-state cost is
+0.68 s over a stock sandbox, measured separately. Only the first create of a new image
pays the pull.

## Pinning

A tag moves when the next `template-v*` is cut; a digest does not. For anything
reproducible, pin:

```
ghcr.io/ola-krutrim/sandbox-aider@sha256:012c54d00ecac34402f1f657c224861aece38bc38502f0a9e91580048f6ae61f
ghcr.io/ola-krutrim/sandbox-browser-playwright@sha256:f6ab09812c925cc72b9744cb4ff138776d3a33f709c2fc5ea2b1abe6c85ed3c6
ghcr.io/ola-krutrim/sandbox-bun@sha256:c330a31f24518696dbb7e4e8794a45dfa270253b2777117e2b44bb1f60104baf
ghcr.io/ola-krutrim/sandbox-claude-code@sha256:064615279f6e983e8f20af323b0df65e7371f74a798168af2be1588ce602a8c6
ghcr.io/ola-krutrim/sandbox-code-interpreter@sha256:7d3fd5ba041773ce3e4fe18262cff72713b37bf1ffeddd9c3fd2d3856d0fa0dd
ghcr.io/ola-krutrim/sandbox-codex@sha256:0e149b8ae7b5042c7ac0d62d0343399e15869d6fcc46c473fc421061f535ee1b
ghcr.io/ola-krutrim/sandbox-computer-use@sha256:1fa50fd3c1a7fad6d5b0179e30bda42d1d4baccfcad396d9055132a45e653ad8
ghcr.io/ola-krutrim/sandbox-data-science@sha256:ca3b85a7fa2932228416380c80c8d6a1caee86a87108613cbcdf9ed1c4b3b8a6
ghcr.io/ola-krutrim/sandbox-database@sha256:25e6aeb99b3d797c986db70098e22b66cc8178a30f6607e83eb242bbd9e07e22
ghcr.io/ola-krutrim/sandbox-deno@sha256:c7a5117bf20af06acff235adc183d884422ec26abd969b0e32769c076e396ca8
ghcr.io/ola-krutrim/sandbox-documents@sha256:237cf1573ee7242c65938247720606c6b7c27ea80dddd1e489621056040e5802
ghcr.io/ola-krutrim/sandbox-ffmpeg@sha256:569ef84e18dce8c421887bcb711fca8ec90aafa7b5bf7f8cf6289be8d8a60593
ghcr.io/ola-krutrim/sandbox-golang@sha256:c7a4ebe70991776df62118e12743030e5398e73c2896f7b35f7d9bef75627130
ghcr.io/ola-krutrim/sandbox-hermes@sha256:2222138690252211a82acc3ba973b5febb3d88c530ea57b52dc4d6842ceeaa75
ghcr.io/ola-krutrim/sandbox-java@sha256:4cec119d57cc84325f8f4f66aec117f4af2e820a64500f2ddccb79a4de726d2f
ghcr.io/ola-krutrim/sandbox-nodejs@sha256:ac79ad21c431079142cefc863678e392d1cb4fd41113e9a05e593f65639ef2c2
ghcr.io/ola-krutrim/sandbox-opencode@sha256:6c4daef579b299a131123b3cb954789803197ddba6f543dcd8b7682f6c249b6c
ghcr.io/ola-krutrim/sandbox-php@sha256:614393ca58a774442ecafd36db374d85dbec00696b79689a7c9fa11e4c6ede8f
ghcr.io/ola-krutrim/sandbox-ruby@sha256:a24c89dfee176361c04100f4749b8064274c2debf640992876ce7c1e6d3b639b
ghcr.io/ola-krutrim/sandbox-rust@sha256:63d470ee2d1f0c001c251eddb69a37c24b3fe732903f8f8120ec0d5e016ea4c3
ghcr.io/ola-krutrim/sandbox-terminal-bench@sha256:4d7bd7d5a0c240ee5f5c7cf62ec717fbbeb5700d16192dec8369e52e003d6df4
```

## Hermes Agent: PyPI, not the official installer

Hermes Agent offers two install paths. Both were run in a sandbox before choosing:

| path | time | size | result |
|---|---|---|---|
| `pip install hermes-agent==0.19.0` | 41 s | 189 MB | v0.19.0 on Python 3.12, `--version` and `--help` exit 0 |
| official `install.sh` | 750 s | 2.7 GB | v0.22.2, stages its own Python 3.14 |

The template uses PyPI. The installer stages a second Python and 58 bundled skills,
which is where the 2.7 GB goes; it also publishes its launcher under
`/root/.local/bin` — unreachable once the image drops to UID 1000 — appends to shell
rc files, and enables a background skill curator. Its `cua-driver` step failed outright
on a missing `libX11.so.6`. None of that belongs in an ephemeral sandbox image.

The cost is version lag: PyPI carries 0.19.0 while the repo is at v0.22.2. `hermes
update` moves a running sandbox forward.

One measured caveat, relevant to the UID 1000 question in #168. On a UID with no
`/etc/passwd` entry **and `HOME` unset**, the CLI raises
`RuntimeError: Could not determine home directory.` at import and exits 1, in
`hermes_constants._get_platform_default_hermes_home`. `HERMES_HOME` does not rescue it,
because the lookup precedes the override — but **setting `HOME` does**, with no
`HERMES_HOME` needed. `sandbox-base` therefore sets `HOME=/app`, which protects every
template, not just this one.

Two corrections to an earlier version of this note. It gave the exit code as 120; that
was an artefact of piping the output through `head`, which closes the pipe and makes
CPython fail to flush stdout at exit. And it implied `HERMES_HOME` was the mitigation,
which sent the fix to the wrong layer. The mechanism was found by @buzz_agent_runtime,
whose own image survives this because it sets `ENV HOME` explicitly.

## The base image

Every template builds `FROM ghcr.io/ola-krutrim/sandbox-base`. The base carries the
BYOC contract — the `sandbox-agent` binary, port 8871, `/app` owned by UID 1000 — and a
template adds only its own tools.

This is worth keeping. Shared base layers dedupe in the registry rather than being
stored twenty-one times, the base is cached on the node after the first pull so each
additional template costs little beyond its own layer, and a CVE in the base is patched
in one Dockerfile instead of twenty-one.

The build is two-phase: `sandbox-base` first, then every template against it, pinned
with `BASE_TAG` so a tagged release is reproducible.

## These images must be public

The platform pulls **anonymously** — private registries and pull credentials are not
supported. A private package cannot be used at all. The publish workflow verifies the
anonymous pull path explicitly (logging out of GHCR first), because an authenticated
test would pass while the real path fails.

`ola-krutrim` forbade public packages at the organisation level until an owner
relaxed that policy; publishing a usable template depends on it staying relaxed. Each
package's visibility is then set once by hand, because GitHub exposes no REST endpoint
for it — a PATCH returns 404. The workflow therefore prints the settings URL per
template instead of pretending to set it, and the `verify` job names every template
that is not anonymously pullable.

## What a template costs at create time

The table above gives one cold create per template. This section is the controlled
measurement that explains those numbers, taken for `computer-use` on `sandbox-large` in
In-Bangalore-1, create → usable, with stock-image controls in the same run:

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

### The warm penalty does not scale with image size

Measured by alternating the smallest and largest templates, 8 s apart, with stock
controls in the same run:

| image | MiB compressed | n | median |
|---|---|---|---|
| `terminal-bench` | 93 | 6 | 2.59 s |
| `browser-playwright` | 950 | 6 | 2.45 s |
| stock control | — | 3 | 1.64 s |

A 10x difference in image size costs nothing measurable once the image is resident:
+0.95 s for the small one, +0.81 s for the large one. Budget about a second for any
template here, including the browser ones.

This also settles the cache-scope doubt the earlier measurement left open. Both images
had been pulled into the region earlier; every spaced create was fast, so residency is
not per-create chance.

### Creates in a burst are throttled, and the error does not say so

Twenty-one creates issued back to back, with no spacing, produced seven in the 12–42 s
range and two failures — one a raw `403 Forbidden` **HTML** page that the SDK surfaces as
`PermissionDeniedError`, one a timeout. The same images 8 s apart produced fifteen clean
creates with nothing above 6.5 s. Stock controls were unaffected in both runs, and the
slow creates were uncorrelated with image size, so this is request rate, not image pull.

If you start sandboxes in a loop, space them. A `PermissionDeniedError` from a burst is
almost certainly a rate limit, not a credentials problem — and because it is a 403 rather
than a 429, a normal retry policy will not retry it. Tracked as
ola-silicon/Krutrim-Cloud-Service-Omni#171.

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
