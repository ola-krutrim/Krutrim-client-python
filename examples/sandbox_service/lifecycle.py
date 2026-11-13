"""Run against an explicitly chosen gateway. Creates a billable sandbox and deletes it on exit."""

from __future__ import annotations

import sys
import argparse
from uuid import uuid4

from krutrim_client import KrutrimClient
from krutrim_client.types.sandbox_service import SandboxResponse


def wait_for(client: KrutrimClient, response: SandboxResponse, region: str) -> None:
    if response.details.operation_id:
        client.sandbox.operations.wait(response.details.operation_id, x_region=region)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="Gateway origin, e.g. https://cloud.olakrutrim.com")
    parser.add_argument("--region", default="In-Bangalore-1")
    parser.add_argument("--flavor", required=True, help="Select from client.sandbox.flavors.list")
    parser.add_argument("--template", default="python")
    args = parser.parse_args()
    # KRUTRIMCLIENT_API_KEY must contain an IAM access token.
    with KrutrimClient(base_url=args.base_url) as client:
        created = client.sandbox.sandboxes.create(
            name="sdk-example-" + uuid4().hex[:8],
            flavor=args.flavor,
            template=args.template,
            ttl_seconds=600,
            x_region=args.region,
            env={"GREETING": "namaste"},
        )
        krn = created.details.krn_id
        try:
            wait_for(client, created, args.region)
            output = client.sandbox.sandboxes.exec(krn_id=krn, x_region=args.region, cmd="echo $GREETING")
            sys.stdout.write(output.details.stdout)
            # Inspect output.details.exit_code even when the HTTP call succeeded.
            client.sandbox.files.upload(
                krn_id=krn, x_region=args.region, path="/tmp/sdk-example.bin", content=b"\x00\xffhello"
            )
            with client.sandbox.files.with_streaming_response.download(
                krn_id=krn,
                x_region=args.region,
                path="/tmp/sdk-example.bin",
            ) as response:
                assert b"".join(response.iter_bytes()) == b"\x00\xffhello"
            wait_for(client, client.sandbox.sandboxes.stop(krn_id=krn, x_region=args.region), args.region)
            wait_for(client, client.sandbox.sandboxes.start(krn_id=krn, x_region=args.region), args.region)
        finally:
            wait_for(client, client.sandbox.sandboxes.delete(krn_id=krn, x_region=args.region), args.region)


if __name__ == "__main__":
    main()
