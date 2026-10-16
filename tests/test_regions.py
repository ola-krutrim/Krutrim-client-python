from __future__ import annotations

import pytest

from krutrim_client import SUPPORTED_REGIONS, Region, KrutrimClient, AsyncKrutrimClient
from krutrim_client._regions import extract_region_from_krn, unsupported_region_error

API_KEY = "test-api-key"


def _validate_asg_region(resource: object, region: Region) -> None:
    resource.validate_create_asg_parameters(  # type: ignore[attr-defined]
        asg_name="asg",
        image_krn="image-krn",
        instance_name="instance",
        subnet_id="subnet-id",
        max=2,
        min=1,
        save_as_template=False,
        vpc_krn="vpc-krn",
        vpc_name="vpc",
        x_region=region,
        launch_from_template=False,
    )


@pytest.mark.parametrize("region", SUPPORTED_REGIONS)
def test_all_sync_service_validators_accept_supported_regions(region: Region) -> None:
    client = KrutrimClient(api_key=API_KEY)

    client.highlvlvpc.validate_delete_instance_parameters("instance-krn", False)
    # delete_instance derives region from the KRN; verify the extraction accepts all supported regions
    assert extract_region_from_krn(f"krn:vm:{region}:acct:cust:instance:id") == region
    client.kbs.validate_delete_volume_parameters("volume-id", "tenant-id", region)
    client.securityGroup.validate_create_security_group_parameters("description", "name", "vpc-id", region)
    client.startStopVM.validate_perform_action_parameters("instance-krn", "start", region)
    client.lb.validate_region(region)
    _validate_asg_region(client.asgV1, region)


@pytest.mark.asyncio
@pytest.mark.parametrize("region", SUPPORTED_REGIONS)
async def test_all_async_service_validators_accept_supported_regions(region: Region) -> None:
    client = AsyncKrutrimClient(api_key=API_KEY)

    client.highlvlvpc.validate_delete_instance_parameters("instance-krn", False)
    assert extract_region_from_krn(f"krn:vm:{region}:acct:cust:instance:id") == region
    await client.kbs.validate_delete_volume_parameters("volume-id", "tenant-id", region)
    await client.securityGroup.validate_create_security_group_parameters("description", "name", "vpc-id", region)
    await client.startStopVM.validate_perform_action_parameters("instance-krn", "start", region)
    await client.lb.validate_region(region)
    _validate_asg_region(client.asgV1, region)


def test_supported_regions_public_api() -> None:
    assert SUPPORTED_REGIONS == (
        "In-Hyderabad-2",
        "In-Hyderabad-1",
        "In-Bangalore-1",
    )


def test_services_reject_unsupported_region() -> None:
    client = KrutrimClient(api_key=API_KEY)
    with pytest.raises(ValueError, match="must be one of"):
        client.lb.validate_region("In-Delhi-1")
    with pytest.raises(ValueError, match="must be one of"):
        client.startStopVM.validate_perform_action_parameters("instance-krn", "start", "In-Delhi-1")
