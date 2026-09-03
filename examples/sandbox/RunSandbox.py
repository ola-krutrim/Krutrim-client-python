from __future__ import annotations

import os
import json

from krutrim_client import KrutrimClient

WORKSPACE = "/app/work"


def required_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Set {name} before running this example")
    return value


def agent_program() -> str:
    return (
        "import json, sys\n"
        "source, destination = sys.argv[1:]\n"
        "data = json.load(open(source))\n"
        "json.dump({'result': data['value'] * 2}, open(destination, 'w'))\n"
    )


def main() -> None:
    with KrutrimClient() as client:
        with client.sandbox.create(
            flavor_name=required_environment("KRUTRIM_SANDBOX_FLAVOR"),
            region=required_environment("KRUTRIM_SANDBOX_REGION"),
            timeout=900,
        ) as sandbox:
            print("Sandbox active:", sandbox.sandbox_id)
            sandbox.files.make_dir(WORKSPACE)
            sandbox.files.write(f"{WORKSPACE}/program.py", agent_program())
            sandbox.files.write(f"{WORKSPACE}/input.json", json.dumps({"value": 21}))

            execution = sandbox.run_command(
                "python3 program.py input.json output.json",
                cwd=WORKSPACE,
                timeout=120,
            )
            if execution.exit_code != 0 or execution.timed_out:
                raise RuntimeError(f"agent program failed:\nstdout: {execution.stdout}\nstderr: {execution.stderr}")

            raw_output = sandbox.files.read(f"{WORKSPACE}/output.json")
            if not isinstance(raw_output, str):
                raise RuntimeError("expected the agent result to be UTF-8 JSON")
            print("Agent result:")
            print(json.dumps(json.loads(raw_output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
