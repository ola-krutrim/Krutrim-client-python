# Changelog

All notable changes to `krutrim_client` are recorded here.

This file starts at 0.8.5. Releases 0.6.2 through 0.8.4 were published to PyPI
without git tags, GitHub releases, or changelog entries, so what shipped in each
of them cannot be reconstructed from this repository. The tags are being added
retroactively from the `releaseversion` commits; until that is done, treat PyPI
as the record of what exists and this file as the record of what changed.

## 0.8.5 — unreleased

### Changed — the sandbox network-policy parameters are now refused

`sandbox.api.create()` and `sandbox.api.update_network_policy()` raise
`NotImplementedError` when given `allow_internet_access`,
`outbound_cidr_allowlist`, `outbound_domain_allowlist`, or
`inbound_cidr_allowlist`.

The service accepts all four, echoes them back in the `update_network_policy`
response, and enforces none of them. A sandbox created with
`allow_internet_access=False` still reaches the public internet, and `retrieve()`
reports no policy at all, so a caller has no way to detect this from the API: the
write claims a restriction and the read is silent. Measured on In-Bangalore-1 on
2026-10-19 and tracked as Omni #169.

Refusing is deliberate. These parameters fail *open*, which makes them worse than
an absent feature — an absent feature cannot be mistaken for isolation. They were
never in a released version, so nothing that works today stops working.

Set `KRUTRIM_ALLOW_UNENFORCED_NETWORK_POLICY=1` to send them anyway for
service-side testing. Remove the guard in `resources/sandbox/_helpers.py` once
enforcement ships — not before.

### Changed — environment variable resolution (Omni #180)

Both the API key and the base URL are now read from any of four names, and two
names holding **different** values is an error rather than a silent preference:

| Setting | Names honoured (canonical first) |
|---|---|
| API key | `KRUTRIMCLIENT_API_KEY`, `KRUTRIM_API_KEY`, `KRUTRIM_CLIENT_API_KEY`, `krutrim_client_API_KEY` |
| Base URL | `KRUTRIMCLIENT_BASE_URL`, `KRUTRIM_BASE_URL`, `KRUTRIM_CLIENT_BASE_URL`, `krutrim_client_BASE_URL` |

This aligns the SDK with `krutrim_mcp_server`, which already accepted the four
key names and already failed closed on a conflict. Previously the SDK read only
`KRUTRIMCLIENT_API_KEY`, so a key configured the way the MCP server documents
produced an **unauthenticated client**, and only `KRUTRIMCLIENT_BASE_URL`, so a
base URL set under any other name was ignored in silence and the request went to
production.

**Behaviour change:** `KrutrimClient` now raises `KrutrimClientError` when no API
key is available, which `AsyncKrutrimClient` already did. It previously defaulted
to `api_key = ""` and sent no `Authorization` header, so the first request failed
at the gateway with `400 {"message":"Authorization header is missing"}` — a
service-shaped error for a local misconfiguration. Code that constructs a sync
client without a key and never uses it will now raise at construction.

### Fixed

- **`AsyncHighlvlvpcResource.create_vpc()` raised `TypeError` on every call.** It
  invoked `validate_create_vpc_parameters()` without `x_region`, which that
  validator requires positionally, so the async VPC-creation path was unusable in
  0.8.4 as published. The synchronous path was unaffected — it passed
  `x_region` correctly. One-line fix; reproduced against a clean install of
  0.8.4 from PyPI before fixing.

### Added

- **`.github/workflows/tests.yml`** — the test suite now runs in CI, on pushes to
  `main` and on pull requests, against Python 3.9 and 3.12. There was previously
  no workflow that ran `pytest`; the only workflow built container images. That
  gap is why the `create_vpc` defect above shipped, and why 28 tests were failing
  on `main` at the time this was written.
- A **version-consistency job**, because the version is declared in both
  `pyproject.toml` and `src/krutrim_client/_version.py` and has drifted before.
- **`tests/sample_file.txt`**, a fixture `tests/test_transform.py` has always
  required but which was never committed.

### Fixed — tests

These were failing on `main`, independently of any change above:

- `tests/test_client.py` called `highlvlvpc.create_vpc(k_customer_id=…,
  x_account_id=…)`, parameters that method has not accepted since the
  `highlvlvpc` refactor that shipped in 0.8.4. Updated to the current signature,
  with one shared payload that satisfies `validate_create_vpc_parameters`.
- `test_base_url_env` set `krutrim_client_BASE_URL` and asserted it took effect,
  but the client read only `KRUTRIMCLIENT_BASE_URL`. Both names now work, per the
  environment-variable change above.

### Known issues, unchanged by this release

- `test_copy_build_request` is a `tracemalloc` leak detector whose result depends
  on the allocation history of whatever ran before it. It is deselected in CI,
  with the reason recorded in the workflow, and still runs locally. It needs to
  be stabilised or removed rather than left deselected.
- `sandbox.api.proxy.request()` takes no port and reaches only the sandbox
  runtime's health endpoint, so it cannot proxy to a caller's own service. Omni
  #179.
- `ports.open()` returns a relative path in a field named `url`, and the
  forwarded endpoint requires an `Authorization` header, so the URL cannot be
  shared. Omni #178.
