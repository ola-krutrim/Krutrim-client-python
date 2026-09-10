"""Cookbook: explicit sandbox lifecycle management.

1. Discover flavors and templates before creating anything.
2. Create a sandbox without a context manager (manual ownership).
3. Reattach to the same sandbox by ID with `connect`.
4. Check liveness, extend the TTL, and delete explicitly with `kill`.

Use this pattern when a sandbox outlives a single code block — for example a
job started by one process and finished or monitored by another.
"""

from __future__ import annotations

import os
import time

from krutrim_client import KrutrimClient

DELETE_DEADLINE = 120  # seconds to wait for asynchronous deletion


def required_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Set {name} before running this example")
    return value


def main() -> None:
    region = required_environment("KRUTRIM_SANDBOX_REGION")
    flavor = required_environment("KRUTRIM_SANDBOX_FLAVOR")

    with KrutrimClient() as client:
        # 1. Discovery: what can we create here? Live flavor payloads carry
        #    the name inside `group_by`.
        flavors = client.sandbox.api.list_flavors(region=region).data or []
        print(f"Flavors in {region} ({len(flavors)} total):")
        for item in flavors[:5]:
            group = item.group_by
            print("  -", item.name or (group.flavorname if group else None))

        templates = client.sandbox.api.list_templates()
        print(f"Templates ({len(templates)} total):")
        for template in templates[:5]:
            print("  -", template.template_name)

        # 2. Manual lifecycle: without a context manager, deletion is our job,
        #    so everything after create runs under try/finally.
        sandbox = client.sandbox.create(flavor_name=flavor, region=region, timeout=300)
        try:
            metadata = sandbox.metadata
            print("\nCreated:", sandbox.sandbox_id)
            print("  status:    ", metadata.status)
            print("  flavor:    ", metadata.flavor_name)
            print("  ttl:       ", metadata.ttl_seconds, "seconds")
            print("  expires at:", metadata.expires_at)

            # 3. Reattach by ID — how a second process would pick up this
            #    sandbox. `connect` waits until the sandbox is active.
            reconnected = client.sandbox.connect(sandbox.sandbox_id)
            result = reconnected.run_command("echo hello from a reconnected handle", timeout=30)
            print("\nReconnected handle says:", result.stdout.strip())

            # 4. Liveness and TTL extension. `set_timeout` resets the expiry
            #    deadline to now + N seconds; it is not additive.
            print("Running:", sandbox.is_running())
            sandbox.set_timeout(900)
            print("Expires at after set_timeout(900):", sandbox.metadata.expires_at)
        finally:
            # 5. Explicit, idempotent deletion. `kill` requests asynchronous
            #    deletion; poll `is_running` to observe it complete.
            sandbox.kill()

        deadline = time.monotonic() + DELETE_DEADLINE
        while sandbox.is_running():
            if time.monotonic() > deadline:
                raise RuntimeError(f"sandbox still running {DELETE_DEADLINE} seconds after kill")
            time.sleep(2)
        print("\nSandbox deleted, is_running() ->", False)


if __name__ == "__main__":
    main()
