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


def extract_region_from_krn(krn: str, parameter: str = "instanceKrn") -> str:
    """Derive the region of a resource from its KRN.

    KRNs follow the format ``krn:<type>:<region>:<account>:<customer>:<resource_type>:<id>``,
    so the region is always the third colon-separated segment. Deriving the region
    from the KRN (instead of accepting it as a separate, user-supplied parameter)
    guarantees requests can never target a region that mismatches the resource.
    """
    if not isinstance(krn, str) or not krn.strip():
        raise ValueError(f"'{parameter}' must be a non-empty string.")

    segments = krn.split(":")
    if len(segments) < 3 or not segments[2].strip():
        raise ValueError(f"'{parameter}' is not a valid KRN; unable to determine its region.")

    region = segments[2]
    if region not in SUPPORTED_REGIONS:
        raise unsupported_region_error("region")

    return region
