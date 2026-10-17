# Smoke tests

A template's job is not to report a version. It is to do the work.

`template-v1.2.0` shipped a `rust` image where `rustc --version` was correct and
`cargo build` failed with ``linker `cc` not found`` — no C linker existed in the image.
Every CI job was green, because the publish workflow asserted the **contract** (`/app`,
UID, port, `HOME`, a live health response) and never asserted **capability**.

A smoke test closes that gap. If `templates/<name>/smoke.sh` exists, the publish
workflow runs it inside the freshly built image and fails the build on a non-zero exit.

Rules that keep these honest:

- **Produce an artifact or compute a result.** `--version` is not a smoke test; it is
  the thing that let the rust defect ship.
- **Exit non-zero on failure.** Run under `set -euo pipefail`. Do not append `|| true`,
  and do not pipe the thing under test into `head` or `grep -q` — a closed pipe reports
  its own status, which is how real failures get swallowed.
- **Keep it under a minute** and free of network access where possible, so a registry
  outage does not read as a broken template.
