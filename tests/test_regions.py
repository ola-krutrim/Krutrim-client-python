from __future__ import annotations

from typing import Type, Callable

import pytest

from krutrim_client._constants import SUPPORTED_REGIONS
from krutrim_client.resources.lb.lb import HighlvlResource, AsyncHighlvlResource
from krutrim_client.resources.asg.asgV1 import V1Resource, AsyncV1Resource
from krutrim_client.resources.highlvlvpc import HighlvlvpcResource


@pytest.mark.parametrize("region", SUPPORTED_REGIONS)
def test_load_balancer_supports_region(region: str) -> None:
    resource = object.__new__(HighlvlResource)

    resource.validate_region(region)


@pytest.mark.parametrize("region", SUPPORTED_REGIONS)
async def test_async_load_balancer_supports_region(region: str) -> None:
    await AsyncHighlvlResource.validate_region(region)


@pytest.mark.parametrize("region", SUPPORTED_REGIONS)
def test_highlvlvpc_supports_region(region: str) -> None:
    resource = object.__new__(HighlvlvpcResource)

    resource.validate_create_image_parameters("image", "instance-krn", region)
    resource.validate_upload_image_s3_parameters(region, "qcow2", "https://example.com/image")


@pytest.mark.parametrize("resource_type", [V1Resource, AsyncV1Resource])
@pytest.mark.parametrize("region", SUPPORTED_REGIONS)
def test_asg_supports_region(resource_type: Type[V1Resource] | Type[AsyncV1Resource], region: str) -> None:
    resource = object.__new__(resource_type)

    resource.validate_create_asg_parameters(
        asg_name="asg",
        image_krn="image-krn",
        instance_name="instance",
        subnet_id="subnet",
        max=2,
        min=1,
        save_as_template=False,
        vpc_krn="vpc-krn",
        vpc_name="vpc",
        x_region=region,
        launch_from_template=False,
    )
    resource.validate_create_launch_template_parameters(
        image_krn="image-krn",
        instance_name="instance",
        instance_type="CPU-1x-4GB",
        max=2,
        min=1,
        vpc_name="vpc",
        region=region,
        security_groups=[],
        sshkey_name="ssh-key",
        subnet_id="subnet",
        template_name="template",
        volume_size=[],
        volume_name="volume",
        volume_type="standard",
        vpc_krn="vpc-krn",
        x_region=region,
    )


@pytest.mark.parametrize("region", [*SUPPORTED_REGIONS, "colo-1"])
def test_asg_update_launch_template_preserves_supported_regions(region: str) -> None:
    resource = object.__new__(V1Resource)

    resource.validate_update_launch_template_parameters(
        template_id="template-id",
        template_name="template",
        instance_name="instance",
        instance_type="CPU-1x-4GB",
        sshkey_name="ssh-key",
        image_krn="image-krn",
        security_groups=[],
        min=1,
        max=2,
        volume_size=[],
        x_region=region,
    )


@pytest.mark.parametrize(
    "validator",
    [
        lambda: object.__new__(HighlvlResource).validate_region("In-Delhi-1"),
        lambda: object.__new__(HighlvlvpcResource).validate_create_image_parameters(
            "image", "instance-krn", "In-Delhi-1"
        ),
    ],
)
def test_services_reject_unsupported_region(validator: Callable[[], None]) -> None:
    with pytest.raises(ValueError, match="In-Hyderabad-1"):
        validator()
