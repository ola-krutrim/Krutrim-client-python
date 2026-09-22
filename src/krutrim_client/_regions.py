from __future__ import annotations

from typing_extensions import Literal

Region = Literal["In-Hyderabad-2", "In-Hyderabad-1", "In-Bangalore-1"]

SUPPORTED_REGIONS: tuple[Region, ...] = (
    "In-Hyderabad-2",
    "In-Hyderabad-1",
    "In-Bangalore-1",
)


def unsupported_region_error(parameter: str = "x_region", *additional_regions: str) -> ValueError:
    supported_regions = (*SUPPORTED_REGIONS, *additional_regions)
    formatted_regions = ", ".join(repr(region) for region in supported_regions)
    return ValueError(f"'{parameter}' must be one of: {formatted_regions}.")
