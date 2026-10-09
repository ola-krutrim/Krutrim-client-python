from __future__ import annotations

import os

from krutrim_client import KrutrimClient


def required_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value or not value.strip():
        raise RuntimeError(f"Set {name} before running this example")
    return value


def main() -> None:
    image_uri = required_environment("KRUTRIM_SANDBOX_IMAGE")
    region = required_environment("KRUTRIM_SANDBOX_REGION")
    flavor_name = required_environment("KRUTRIM_SANDBOX_FLAVOR")

    with KrutrimClient() as client:
        with client.sandbox.create(
            image_uri=image_uri,
            region=region,
            flavor_name=flavor_name,
            timeout=900,
            wait_timeout=300,
        ) as sandbox:
            print("Sandbox active:", sandbox.sandbox_id)
            print("Resolved image:", sandbox.metadata.image_uri)

            execution = sandbox.run_command(
                "python3 -c 'import sys, requests; print(sys.version); print(requests.__version__)'",
                cwd="/app",
                timeout=60,
            )
            if execution.timed_out or execution.exit_code != 0:
                raise RuntimeError(
                    "custom image dependency check failed "
                    f"(exit_code={execution.exit_code}, timed_out={execution.timed_out}):\n"
                    f"stdout: {execution.stdout}\nstderr: {execution.stderr}"
                )
            print("Runtime and baked-in requests version:")
            print(execution.stdout)

            message = "hello from a custom image\n"
            sandbox.files.write("/app/message.txt", message)
            downloaded = sandbox.files.read("/app/message.txt")
            if downloaded != message:
                raise RuntimeError("uploaded message did not round-trip correctly")
            print("File round-trip:", downloaded.rstrip())


if __name__ == "__main__":
    main()
