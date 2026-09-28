"""Manual test for issue #143.

Lists all sandboxes on the account and deletes each one using the
`sandbox_id` attribute on list rows — the exact repro from the issue.
Before the fix this raised:

    ValueError: Expected a non-empty sandbox identifier but received None

Usage:
    export KRUTRIMCLIENT_API_KEY="..."
    python examples/sandbox/cookbook/cleanup_sandboxes/main.py
"""

from __future__ import annotations

from krutrim_client import KrutrimClient


def main() -> None:
    with KrutrimClient() as client:
        rows = client.sandbox.api.list(limit=50).data.rows or []
        print(f"Found {len(rows)} sandbox(es)")

        for r in rows:
            print(f"  id={r.id!r} sandbox_id={r.sandbox_id!r} krn={r.krn!r}")
            assert r.sandbox_id == r.id, "sandbox_id should alias id"

            # Uncomment to actually delete:
            # client.sandbox.api.delete(r.sandbox_id)
            # print(f"  deleted {r.sandbox_id}")


if __name__ == "__main__":
    main()
