"""Cookbook: a small data pipeline over sandbox files.

1. Upload a CSV and a transform script (`sandbox.files.write`).
2. Run the transform inside the sandbox (`sandbox.run_command`).
3. Inspect outputs with `sandbox.files.list` and `sandbox.files.stat`.
4. Download the JSON report as text and the gzip archive as exact bytes
   (`sandbox.files.read(..., format="bytes")`), then verify it locally.

Everything inside the sandbox uses only the Python standard library.
"""

from __future__ import annotations

import os
import gzip
import json

from krutrim_client import KrutrimClient

WORKSPACE = "/app/work"

SALES_CSV = """\
order_id,category,quantity,unit_price
1001,books,2,349.00
1002,electronics,1,24999.00
1003,books,5,199.00
1004,grocery,10,89.50
1005,electronics,2,1499.00
1006,grocery,4,120.00
"""


def required_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Set {name} before running this example")
    return value


def transform_program() -> str:
    """Aggregate revenue per category; emit a JSON report and a gzip archive."""
    return """\
import csv, gzip, json

rows = list(csv.DictReader(open("sales.csv")))
totals = {}
for row in rows:
    revenue = float(row["quantity"]) * float(row["unit_price"])
    totals[row["category"]] = totals.get(row["category"], 0.0) + revenue

json.dump(
    {"orders": len(rows), "revenue_by_category": totals},
    open("report.json", "w"),
    indent=2,
    sort_keys=True,
)

with gzip.open("report.csv.gz", "wt", newline="") as archive:
    writer = csv.writer(archive)
    writer.writerow(["category", "revenue"])
    for category in sorted(totals):
        writer.writerow([category, f"{totals[category]:.2f}"])
"""


def main() -> None:
    with KrutrimClient() as client:
        with client.sandbox.create(
            flavor_name=required_environment("KRUTRIM_SANDBOX_FLAVOR"),
            region=required_environment("KRUTRIM_SANDBOX_REGION"),
            timeout=900,
        ) as sandbox:
            print("Sandbox active:", sandbox.sandbox_id)

            # 1. Upload the input data and the transform script.
            sandbox.files.make_dir(WORKSPACE)
            sandbox.files.write(f"{WORKSPACE}/sales.csv", SALES_CSV)
            sandbox.files.write(f"{WORKSPACE}/transform.py", transform_program())

            # 2. Run the pipeline step; the result is data even on failure.
            execution = sandbox.run_command("python3 transform.py", cwd=WORKSPACE, timeout=60)
            if execution.exit_code != 0 or execution.timed_out:
                raise RuntimeError(f"transform failed:\nstdout: {execution.stdout}\nstderr: {execution.stderr}")

            # 3. Inspect what the pipeline produced.
            print("\nWorkspace contents:")
            for entry in sandbox.files.list(WORKSPACE):
                print(f"  {entry.type:4}  {entry.size or 0:>6} B  {entry.name}")
            archive_info = sandbox.files.stat(f"{WORKSPACE}/report.csv.gz")
            print("Archive size:", archive_info.size, "bytes")

            # 4a. Text download: read decodes UTF-8 by default.
            report = sandbox.files.read(f"{WORKSPACE}/report.json")
            assert isinstance(report, str)
            print("\nJSON report:")
            print(report)

            # 4b. Binary download: format="bytes" returns the exact bytes.
            archive = sandbox.files.read(f"{WORKSPACE}/report.csv.gz", format="bytes")
            assert isinstance(archive, bytes)
            with open("report.csv.gz", "wb") as local_file:
                local_file.write(archive)
            print("Saved locally: report.csv.gz")
            print("\nDecompressed archive:")
            print(gzip.decompress(archive).decode(), end="")

            # Sanity check: archive totals must match the JSON report.
            totals = json.loads(report)["revenue_by_category"]
            print("\nCategories in report:", ", ".join(sorted(totals)))


if __name__ == "__main__":
    main()
