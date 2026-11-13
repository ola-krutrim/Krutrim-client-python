"""Exercise optional customer features on an existing ACTIVE sandbox. Uses its compute and changes egress policy."""

from __future__ import annotations

import sys
import time
import argparse
from uuid import uuid4
from typing import cast

from krutrim_client import KrutrimClient
from krutrim_client.types.sandbox_service import NetworkPolicyParams


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--region", default="In-Bangalore-1")
    parser.add_argument("--krn", required=True)
    parser.add_argument("--image", help="Optionally build and delete a customer template from this public amd64 image")
    args = parser.parse_args()
    with KrutrimClient(base_url=args.base_url) as client:
        api, krn, region = client.sandbox, args.krn, args.region
        # List one page; increment offset for subsequent pages.
        api.flavors.list(x_region=region, limit=5, offset=0)
        api.templates.list(x_region=region, limit=5, offset=0)
        if args.image:
            name = "sdk-template-" + uuid4().hex[:8]
            template = api.templates.create(name=name, image=args.image, x_region=region)
            try:
                if template.details.operation_id:
                    api.operations.wait(template.details.operation_id, x_region=region)
                api.templates.retrieve(template_id=name, x_region=region)
            finally:
                api.templates.delete(template_id=name, x_region=region)
        stream = api.sandboxes.exec_stream(krn_id=krn, x_region=region, cmd="echo hello; echo diagnostic >&2")
        with stream:
            for event in stream:
                if event.type == "stdout":
                    sys.stdout.write(event.data)
                elif event.type == "stderr":
                    sys.stderr.write(event.data)
        command = api.commands.create(krn_id=krn, x_region=region, cmd="echo background; sleep 30")
        cid, stdout_offset, stderr_offset = command.details.command_id, 0, 0
        try:
            for _ in range(3):
                output = api.commands.retrieve(
                    krn_id=krn,
                    command_id=cid,
                    x_region=region,
                    stdout_offset=stdout_offset,
                    stderr_offset=stderr_offset,
                    max_bytes=65536,
                ).details
                sys.stdout.write(output.stdout)
                stdout_offset, stderr_offset = output.stdout_offset, output.stderr_offset
                if output.command.status != "running":
                    break
                time.sleep(1)
        finally:
            api.commands.kill(krn_id=krn, command_id=cid, x_region=region)
        original = api.network.retrieve(krn_id=krn, x_region=region).details
        try:
            changed = api.network.update(
                krn_id=krn,
                x_region=region,
                network={"egress": {"default_action": "deny", "allow": ["pypi.org", "files.pythonhosted.org"]}},
            )
            if changed.details.operation_id:
                api.operations.wait(changed.details.operation_id, x_region=region)
        finally:
            restored = api.network.update(
                krn_id=krn, x_region=region, network=cast(NetworkPolicyParams, original.to_dict())
            )
            if restored.details.operation_id:
                api.operations.wait(restored.details.operation_id, x_region=region)
        # Use an available guest port. A program must listen there before requests can succeed.
        exposed = api.ports.expose(krn_id=krn, x_region=region, port=8080, access="token")
        try:
            token_url = exposed.details.url  # Credential URL: do not log it. GET cannot recover it.
            assert token_url
            api.ports.list(krn_id=krn, x_region=region)
            ticket = api.terminal.create_ticket(krn_id=krn, x_region=region).details
            assert ticket.url  # Connect with a WebSocket library within 60 seconds. Do not log the ticket.
        finally:
            api.ports.close(krn_id=krn, x_region=region, port=8080)
        api.sandboxes.usage(krn_id=krn, x_region=region)


if __name__ == "__main__":
    main()
