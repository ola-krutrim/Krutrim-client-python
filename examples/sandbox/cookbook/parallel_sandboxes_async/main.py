"""Cookbook: fan work out to parallel sandboxes and aggregate the results.

Splits a compute job into chunks, runs each chunk in its own sandbox with
`AsyncKrutrimClient` and `asyncio.gather`, and merges the partial results.
Sandbox creation, upload, and execution for all chunks overlap, so total wall
time is close to the slowest single chunk instead of the sum of all chunks.
"""

from __future__ import annotations

import os
import json
import time
import asyncio

from krutrim_client import AsyncKrutrimClient

WORKSPACE = "/app/work"
CHUNKS = [(2, 100_000), (100_001, 200_000), (200_001, 300_000)]

# Counts primes in [lo, hi] with a sieve and reports JSON on stdout.
COUNT_PRIMES = """\
import json, sys, time

lo, hi = int(sys.argv[1]), int(sys.argv[2])
start = time.perf_counter()

sieve = bytearray([1]) * (hi + 1)
sieve[0:2] = b"\\x00\\x00"
p = 2
while p * p <= hi:
    if sieve[p]:
        sieve[p * p :: p] = bytearray(len(sieve[p * p :: p]))
    p += 1

print(json.dumps({
    "lo": lo,
    "hi": hi,
    "primes": sum(sieve[lo:]),
    "elapsed_seconds": round(time.perf_counter() - start, 2),
}))
"""


def required_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Set {name} before running this example")
    return value


async def process_chunk(client: AsyncKrutrimClient, index: int, lo: int, hi: int) -> dict:
    """Create one sandbox, run one chunk, return its parsed result."""
    async with await client.sandbox.create(
        flavor_name=required_environment("KRUTRIM_SANDBOX_FLAVOR"),
        region=required_environment("KRUTRIM_SANDBOX_REGION"),
        timeout=600,
    ) as sandbox:
        print(f"[chunk {index}] sandbox active: {sandbox.sandbox_id}")
        await sandbox.files.make_dir(WORKSPACE)
        await sandbox.files.write(f"{WORKSPACE}/count_primes.py", COUNT_PRIMES)

        execution = await sandbox.run_command(
            f"python3 count_primes.py {lo} {hi}",
            cwd=WORKSPACE,
            timeout=120,
        )
        if execution.exit_code != 0 or execution.timed_out:
            raise RuntimeError(f"chunk {index} failed:\nstdout: {execution.stdout}\nstderr: {execution.stderr}")

        result = json.loads(execution.stdout)
        print(f"[chunk {index}] primes in [{lo:,}, {hi:,}]: {result['primes']:,}")
        return result


async def main() -> None:
    async with AsyncKrutrimClient() as client:
        started = time.perf_counter()
        results = await asyncio.gather(
            *(process_chunk(client, index, lo, hi) for index, (lo, hi) in enumerate(CHUNKS))
        )
        elapsed = time.perf_counter() - started

    total = sum(result["primes"] for result in results)
    compute_seconds = sum(result["elapsed_seconds"] for result in results)
    print(f"\nPrimes below {CHUNKS[-1][1]:,}: {total:,}")
    print(f"Wall time: {elapsed:.1f}s for {len(CHUNKS)} sandboxes (in-sandbox compute: {compute_seconds:.1f}s)")


if __name__ == "__main__":
    asyncio.run(main())
