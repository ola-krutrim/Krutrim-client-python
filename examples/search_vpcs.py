from __future__ import annotations

import os
import json

from dotenv import load_dotenv

from krutrim_client import SUPPORTED_REGIONS, KrutrimClient


def main() -> None:
    load_dotenv()

    api_key = os.environ.get("KRUTRIMCLIENT_API_KEY")
    if not api_key:
        raise RuntimeError("Set KRUTRIMCLIENT_API_KEY in .env before running this example")

    region = os.environ.get("KRUTRIMCLIENT_REGION", "In-Bangalore-1")
    if region not in SUPPORTED_REGIONS:
        supported = ", ".join(SUPPORTED_REGIONS)
        raise RuntimeError(f"KRUTRIMCLIENT_REGION must be one of: {supported}")

    client = KrutrimClient(api_key=api_key)
    response = client.highlvlvpc.with_raw_response.search_vpcs(
        x_region=region,
        size=10,
        page=1,
        status="active",
        sort_by="createdAt",
        order="desc",
        count=False,
    )

    print(f"HTTP {response.status_code}")
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
