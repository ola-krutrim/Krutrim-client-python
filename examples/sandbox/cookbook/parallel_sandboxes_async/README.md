# Parallel sandboxes with the async client

Fan a compute job out to several sandboxes at once with `AsyncKrutrimClient`
and `asyncio.gather`, then aggregate the partial results — the pattern behind
parallel agent evaluation and chunked batch processing.

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

`main.py` counts primes below 300,000 by splitting the range into 3 chunks:

1. `process_chunk` creates one sandbox per chunk — `async with await
   client.sandbox.create(...)` guarantees deletion even if a chunk fails.
2. Each sandbox gets a sieve program via `files.write` and runs it with
   `run_command`; the result comes back as JSON on stdout.
3. `asyncio.gather` overlaps creation, upload, and execution for all chunks,
   so wall time tracks the slowest chunk, not the sum.
4. The host merges the partial counts and reports wall time versus total
   in-sandbox compute time.

If any chunk raises, `asyncio.gather` propagates the first error and every
sandbox still cleans up through its context manager. Pass
`return_exceptions=True` to collect per-chunk failures instead.

## Run

```bash
python main.py
```

Expected output (chunk order may vary):

```
[chunk 0] sandbox active: <sandbox-id>
[chunk 2] sandbox active: <sandbox-id>
[chunk 1] sandbox active: <sandbox-id>
[chunk 0] primes in [2, 100,000]: 9,592
[chunk 1] primes in [100,001, 200,000]: 8,392
[chunk 2] primes in [200,001, 300,000]: 8,013
Primes below 300,000: 25,997
Wall time: <n>s for 3 sandboxes (in-sandbox compute: <n>s)
```
