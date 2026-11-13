"""Async lifecycle example. Creates a billable sandbox and deletes it on exit."""

from __future__ import annotations

import sys
import asyncio
import argparse
from uuid import uuid4
from typing import AsyncIterator

from krutrim_client import AsyncKrutrimClient
from krutrim_client.types.sandbox_service import SandboxResponse


async def wait_for(client: AsyncKrutrimClient, response: SandboxResponse, region: str) -> None:
    if response.details.operation_id:
        await client.sandbox.operations.wait(response.details.operation_id, x_region=region)


async def run(base_url: str, region: str, flavor: str, template: str) -> None:
    async with AsyncKrutrimClient(base_url=base_url) as client:
        created = await client.sandbox.sandboxes.create(
            name="sdk-async-" + uuid4().hex[:8],
            flavor=flavor,
            template=template,
            ttl_seconds=600,
            x_region=region,
        )
        krn = created.details.krn_id
        try:
            await wait_for(client, created, region)
            # A stream is returned after awaiting the request; close it with async with.
            stream = await client.sandbox.sandboxes.exec_stream(
                krn_id=krn,
                x_region=region,
                cmd="echo hello; echo diagnostic >&2",
                timeout_seconds=60,
            )
            async with stream:
                async for event in stream:
                    if event.type == "stdout":
                        sys.stdout.write(event.data)
                    elif event.type == "stderr":
                        sys.stderr.write(event.data)

            async def content() -> AsyncIterator[bytes]:
                yield b"hello "
                yield b"world"

            await client.sandbox.files.upload(
                krn_id=krn, x_region=region, path="/tmp/sdk-example.txt", content=content()
            )
            async with client.sandbox.files.with_streaming_response.download(
                krn_id=krn,
                x_region=region,
                path="/tmp/sdk-example.txt",
            ) as response:
                assert b"".join([chunk async for chunk in response.iter_bytes()]) == b"hello world"
            await wait_for(client, await client.sandbox.sandboxes.stop(krn_id=krn, x_region=region), region)
            await wait_for(client, await client.sandbox.sandboxes.start(krn_id=krn, x_region=region), region)
        finally:
            await wait_for(client, await client.sandbox.sandboxes.delete(krn_id=krn, x_region=region), region)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--region", default="In-Bangalore-1")
    parser.add_argument("--flavor", required=True)
    parser.add_argument("--template", default="python")
    args = parser.parse_args()
    asyncio.run(run(args.base_url, args.region, args.flavor, args.template))


if __name__ == "__main__":
    main()
