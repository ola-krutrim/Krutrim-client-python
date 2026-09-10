# CSV data pipeline with file round-trips

Upload a CSV dataset, transform it inside a sandbox, inspect the outputs, and
download the results — both as text and as exact binary bytes.

## Prerequisites

```bash
pip install krutrim-client
export KRUTRIMCLIENT_API_KEY="<your-api-key>"
export KRUTRIM_SANDBOX_REGION="In-Bangalore-1"
export KRUTRIM_SANDBOX_FLAVOR="sandbox-large"
```

See [../../README.md](../../README.md) for flavor discovery and
[../../../../docs/sandbox.md](../../../../docs/sandbox.md) for the full guide.

## What it does

`main.py` runs a one-step data pipeline (stdlib-only inside the sandbox):

1. Uploads `sales.csv` and `transform.py` with `sandbox.files.write` (UTF-8
   strings; `bytes`, file objects, and local paths work too).
2. Runs the transform with `sandbox.run_command` and checks
   `exit_code`/`timed_out` — command failures are data, not exceptions.
3. Lists the workspace with `sandbox.files.list` and sizes the archive with
   `sandbox.files.stat`.
4. Downloads `report.json` as text (`files.read` decodes UTF-8) and
   `report.csv.gz` as exact bytes (`files.read(..., format="bytes")`), saves
   the archive locally, and decompresses it to verify integrity.

## Run

```bash
python main.py
```

Expected output:

```
Sandbox active: <sandbox-id>

Workspace contents:
  file     ... B  report.csv.gz
  file     ... B  report.json
  file     ... B  sales.csv
  file     ... B  transform.py
Archive size: <n> bytes

JSON report:
{
  "orders": 6,
  "revenue_by_category": { ... }
}
Saved locally: report.csv.gz

Decompressed archive:
category,revenue
books,1693.00
electronics,27997.00
grocery,1375.00

Categories in report: books, electronics, grocery
```

The recipe writes `report.csv.gz` to the current directory as the downloaded
artifact.
