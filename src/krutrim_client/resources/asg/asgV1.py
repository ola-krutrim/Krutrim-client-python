# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Sequence

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, NOT_GIVEN
from ..._utils import maybe_transform, strip_not_given, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.asg import (
    v1_create_asg_params,
    v1_update_asg_params,
    v1_upscale_asg_params,
    v1_retrieve_asg_params,
    v1_downscale_asg_params,
    v1_get_launch_templates_params,
    v1_create_launch_template_params,
    v1_delete_launch_template_params,
    v1_update_launch_template_params,
)
from ..._base_client import make_request_options
from ...types.asg.policy_param import PolicyParam
from ...types.asg.volume_param import VolumeParam

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> V1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/asg-python#accessing-raw-response-data-eg-headers
        """
        return V1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> V1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/asg-python#with_streaming_response
        """
        return V1ResourceWithStreamingResponse(self)
    


    def validate_create_asg_parameters(
        self,
        asg_name,
        image_krn,
        instance_name,
        subnet_id,
        max,
        min,
        save_as_template,
        vpc_krn,
        vpc_name,
        x_region,
        launch_from_template,
        instance_type=None,
        policy=None,
        region=None,
        security_groups=None,
        sshkey_name=None,
        volume_name=None,
        volume_size=None,
        volume_type=None,
        launch_template_version=None,
        launch_template_id=None,
        user_data=None,
        extra_headers=None,
        extra_query=None,
        extra_body=None,
        timeout=None,
    ):
        # 1. Mandatory/Omit-aware String Validation
        for name, value in {
            "asg_name": asg_name,
            "image_krn": image_krn,
            "instance_name": instance_name,
            "subnet_id": subnet_id,
            "vpc_krn": vpc_krn,
            "vpc_name": vpc_name
        }.items():
            if value is not omit:
                if not isinstance(value, str) or not value:
                    raise ValueError(f"'{name}' must be a non-empty string.")

        # 2. Optional String Validation (Fields that default to None)
        optional_strings = {
            "instance_type": instance_type,
            "region": region,
            "sshkey_name": sshkey_name,
            "volume_name": volume_name,
            "volume_type": volume_type,
            "launch_template_id": launch_template_id
        }
        for name, value in optional_strings.items():
            if value not in (None, omit, NOT_GIVEN):
                if not isinstance(value, str) or not value:
                    raise ValueError(f"'{name}' must be a non-empty string if provided.")

        # 3. Validate Booleans
        for name, value in {
            "save_as_template": save_as_template,
            "launch_from_template": launch_from_template,
        }.items():
            if value is not omit and not isinstance(value, bool):
                raise ValueError(f"'{name}' must be a boolean if provided.")

        # 4. Validate Integers
        # Added launch_template_version to integer check
        for name, value in {
            "min": min, 
            "max": max, 
            "launch_template_version": launch_template_version
        }.items():
            if value not in (None, omit, NOT_GIVEN) and not isinstance(value, int):
                raise ValueError(f"'{name}' must be an integer if provided.")

        # 5. Validate Iterables / Sequences
        if policy not in (None, omit, NOT_GIVEN) and not isinstance(policy, (list, tuple, Iterable)):
            raise ValueError("'policy' must be an iterable in the correct format.")

        if security_groups not in (None, omit, NOT_GIVEN) and not isinstance(security_groups, (list, tuple, Sequence)):
            raise ValueError("'security_groups' must be a sequence of strings.")

        if volume_size not in (None, omit, NOT_GIVEN) and not isinstance(volume_size, (list, tuple, Iterable)):
            raise ValueError("'volume_size' must be an iterable in the correct format.")

        # 6. Optional: user_data
        if user_data not in (None, omit, NOT_GIVEN):
            if not isinstance(user_data, (str, dict)):
                raise ValueError("'user_data' must be a string or dictionary if provided.")

        # 7. Optional: extra dicts & timeout
        if extra_headers is not None and not isinstance(extra_headers, dict):
            raise ValueError("'extra_headers' must be a dictionary if provided.")
        if extra_query is not None and not isinstance(extra_query, dict):
            raise ValueError("'extra_query' must be a dictionary if provided.")
        if extra_body is not None and not isinstance(extra_body, dict):
            raise ValueError("'extra_body' must be a dictionary if provided.")

        if timeout not in (None, NOT_GIVEN) and not isinstance(timeout, (int, float, httpx.Timeout)):
            raise ValueError("'timeout' must be a float, int, or httpx.Timeout if provided.")

        # 8. Literal Constraints for x_region
        if x_region is omit or x_region is None:
            raise ValueError("'x_region' is required.")
        
        if x_region != "In-Bangalore-1":
            raise ValueError("'x_region' must be 'In-Bangalore-1'.")

            




    def validate_update_asg_parameters(
        self,
        asg_krn,
        instance_type=None,
        max=None,
        min=None,
        policy=None,
        security_groups=None,
        sshkey_name=None,
        volume_size=None,
        volume_name=None,
        user_data=None,
        extra_headers=None,
        extra_query=None,
        extra_body=None,
        timeout=None,
    ):
    # 1. Mandatory-if-provided Strings (asg_krn, image_krn, instance_type, etc.)
    # We use a tuple for the skip condition to catch all 'empty' states
        skip_conditions = (None, omit, NOT_GIVEN)

        for name, value in {
            "asg_krn": asg_krn,
            "instance_type": instance_type,
            "sshkey_name": sshkey_name,
            "volume_name": volume_name,
        }.items():
            if value not in skip_conditions:
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"'{name}' must be a non-empty string if provided.")

        # 2. Validate Integers (min/max)
        for name, value in {"min": min, "max": max}.items():
            if value not in skip_conditions:
                if not isinstance(value, int):
                    raise ValueError(f"'{name}' must be an integer if provided.")

        # 3. Validate Iterables / Sequences
        iterable_checks = [
            ("policy", policy, (list, tuple, Iterable)),
            ("security_groups", security_groups, (list, tuple, Sequence)),
            ("volume_size", volume_size, (list, tuple, Iterable))
        ]
        for name, value, expected_types in iterable_checks:
            if value not in skip_conditions:
                if not isinstance(value, expected_types):
                    raise ValueError(f"'{name}' must be an iterable in the correct format.")

        # 4. Optional: user_data (string or dict)
        if user_data not in skip_conditions:
            if not isinstance(user_data, (str, dict)):
                raise ValueError("'user_data' must be a string or dictionary if provided.")

        # 5. Optional: extra dicts & timeout
        for name, value in {
            "extra_headers": extra_headers,
            "extra_query": extra_query,
            "extra_body": extra_body
        }.items():
            if value is not None and not isinstance(value, dict):
                raise ValueError(f"'{name}' must be a dictionary if provided.")

        if timeout not in (None, NOT_GIVEN) and not isinstance(timeout, (int, float, httpx.Timeout)):
            raise ValueError("'timeout' must be a float, int, or httpx.Timeout if provided.")


    def validate_create_launch_template_parameters(
        self,
        image_krn,
        instance_name,
        instance_type,
        max,
        min,
        vpc_name,
        region,
        security_groups,
        sshkey_name,
        subnet_id,
        template_name,
        volume_size,
        volume_name,
        volume_type,
        vpc_krn,
        x_region,
        user_data=None,
        policy=None,
        extra_headers=None,
        extra_query=None,
        extra_body=None,
        timeout=None,
    ):
        # 1. Validate String parameters (Non-empty if not omitted)
        for name, value in {
            "image_krn": image_krn,
            "instance_name": instance_name,
            "instance_type": instance_type,
            "vpc_name": vpc_name,
            "region": region,
            "sshkey_name": sshkey_name,
            "subnet_id": subnet_id,
            "template_name": template_name,
            "vpc_krn": vpc_krn,
            "volume_name": volume_name,
            "volume_type":volume_type
        }.items():
            if value is not omit:
                if not isinstance(value, str) or not value:
                    raise ValueError(f"'{name}' must be a non-empty string.")

        # 2. Validate Integers
        for name, value in {"min": min, "max": max}.items():
            if value is not omit and not isinstance(value, int):
                raise ValueError(f"'{name}' must be an integer.")

        # 3. Validate Iterables
        if security_groups is not omit and not isinstance(security_groups, (list, tuple)):
            raise ValueError("'security_groups' must be a list or tuple.")
        
        # volume_size is mandatory in your signature
        if not isinstance(volume_size, (list, tuple, Iterable)):
            raise ValueError("'volume_size' must be an iterable of VolumeParam.")

        # 5. Optional Parameters (user_data and policy)
        if user_data not in (None, NOT_GIVEN):
            if not isinstance(user_data, (str, dict)):
                raise ValueError("'user_data' must be a string or dictionary if provided.")

        if policy not in (None, NOT_GIVEN):
            if not isinstance(policy, (list, tuple, Iterable)):
                raise ValueError("'policy' must be an iterable of PolicyParam if provided.")

        # 6. Extra Dicts & Timeout
        if extra_headers is not None and not isinstance(extra_headers, dict):
            raise ValueError("'extra_headers' must be a dictionary.")
        if extra_query is not None and not isinstance(extra_query, dict):
            raise ValueError("'extra_query' must be a dictionary.")
        if extra_body is not None and not isinstance(extra_body, dict):
            raise ValueError("'extra_body' must be a dictionary.")

        if timeout not in (None, NOT_GIVEN) and not isinstance(timeout, (int, float, httpx.Timeout)):
            raise ValueError("'timeout' must be a float, int, or httpx.Timeout.")

        # 7. Literal Constraints
        if x_region is not omit and x_region not in ("In-Bangalore-1"):
            raise ValueError("'x_region' must be 'In-Bangalore-1'")
        


    def validate_update_launch_template_parameters(
        self,
        template_id,
        template_name,
        instance_name,
        instance_type,
        sshkey_name,
        image_krn,
        security_groups,
        min,
        max,
        volume_size,
        policy=None,
        volume_name=None,
        volume_type=None,
        user_data=None,
        x_region=None,
        extra_headers=None,
        extra_query=None,
        extra_body=None,
        timeout=None,
    ):
        # 1. Mandatory String Parameters (must be non-empty strings)
        for name, value in {
            "template_id": template_id,
            "template_name": template_name,
        }.items():
            if not isinstance(value, str) or not value:
                raise ValueError(f"'{name}' must be a non-empty string.")

        # 2. Optional String Parameters (if not omitted/not given)
        for name, value in {
            "instance_name": instance_name,
            "instance_type": instance_type,
            "sshkey_name": sshkey_name,
            "image_krn": image_krn,
        }.items():
            if value is not omit:
                if not isinstance(value, str) or not value:
                    raise ValueError(f"'{name}' must be a non-empty string.")

        # 3. Handling volume_name and volume_type (NOT_GIVEN check)
        for name, value in {
            "volume_name": volume_name,
            "volume_type": volume_type,
        }.items():
            if value not in (None, NOT_GIVEN):
                if not isinstance(value, str) or not value:
                    raise ValueError(f"'{name}' must be a string if provided.")

        # 4. Integers
        for name, value in {"min": min, "max": max}.items():
            if value is not omit and not isinstance(value, int):
                raise ValueError(f"'{name}' must be an integer if provided.")

        # 5. Iterables (security_groups, volume_size, policy)
        if security_groups is not omit and not isinstance(security_groups, (list, tuple, Iterable)):
            raise ValueError("'security_groups' must be an iterable of strings.")

        if volume_size is not omit and not isinstance(volume_size, (list, tuple, Iterable)):
            raise ValueError("'volume_size' must be an iterable of VolumeParam.")

        if policy not in (None, NOT_GIVEN) and not isinstance(policy, (list, tuple, Iterable)):
            raise ValueError("'policy' must be an iterable of PolicyParam if provided.")

        # 6. user_data
        if user_data not in (None, NOT_GIVEN):
            if not isinstance(user_data, (str, dict)):
                raise ValueError("'user_data' must be a string or dictionary if provided.")

        # 7. Extra Dicts & Timeout
        if extra_headers is not None and not isinstance(extra_headers, dict):
            raise ValueError("'extra_headers' must be a dictionary.")
        if extra_query is not None and not isinstance(extra_query, dict):
            raise ValueError("'extra_query' must be a dictionary.")
        if extra_body is not None and not isinstance(extra_body, dict):
            raise ValueError("'extra_body' must be a dictionary.")

        if timeout not in (None, NOT_GIVEN) and not isinstance(timeout, (int, float, httpx.Timeout)):
            raise ValueError("'timeout' must be a float, int, or httpx.Timeout.")

        # 8. Literal Constraints
        if x_region is not omit and x_region not in ("In-Bangalore-1"):
            raise ValueError("'x_region' must be 'In-Bangalore-1'")
        

    def _fetch_network_id_from_vpc(
        self,
        *,
        vpc_krn: str,
        vpc_name: str,
        x_region: str | None,
        extra_headers: Headers | None,
        timeout: float | httpx.Timeout | None | NotGiven,
    ) -> str:
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x-region": x_region}), **extra_headers}

        api_response = self._get(
            "/v1/highlvlvpc/describe_vpc",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query={
                    "vpc_name": vpc_name,
                    "vpc_id": vpc_krn,
                },
                timeout=timeout,
            ),
            cast_to=dict,
        )

        data = api_response.json()

        vpc_data = next(iter(data.values()))

        return vpc_data["networks"]["krn_id"]

        

    def create_asg(
        self,
        *,
        asg_name: str | Omit = omit,
        vpc_name: str | Omit = omit,
        image_krn: str | Omit = omit,
        instance_name: str | Omit = omit,
        instance_type: str | NotGiven = NOT_GIVEN,
        max: int | Omit = omit,
        min: int | Omit = omit,
        policy: Iterable[PolicyParam] | NotGiven = NOT_GIVEN,
        region: str | NotGiven = NOT_GIVEN,
        save_as_template: bool | Omit = omit,
        security_groups: SequenceNotStr[str] |  NotGiven = NOT_GIVEN,
        sshkey_name: str |  NotGiven = NOT_GIVEN,
        subnet_id: str | Omit = omit,
        volume_name: str | NotGiven = NOT_GIVEN,
        volume_size: Iterable[VolumeParam] | NotGiven = NOT_GIVEN,
        volume_type: str | NotGiven = NOT_GIVEN,
        user_data: str | NotGiven = NOT_GIVEN,
        launch_template_id: str | NotGiven = NOT_GIVEN,
        launch_template_version: int | NotGiven = NOT_GIVEN,
        vpc_krn: str | Omit = omit,
        launch_from_template: bool | Omit = omit,
        x_region: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Auto Scaling Group

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        
        self.validate_create_asg_parameters(
            asg_name=asg_name,
            image_krn=image_krn,
            instance_name=instance_name,
            instance_type=instance_type,
            max=max,
            min=min,
            region=region,
            save_as_template=save_as_template,
            security_groups=security_groups,
            sshkey_name=sshkey_name,
            subnet_id=subnet_id,
            volume_name=volume_name,
            volume_size=volume_size,
            volume_type=volume_type,
            policy=policy,
            vpc_krn=vpc_krn,
            vpc_name=vpc_name,
            launch_from_template=launch_from_template,
            user_data=user_data,
            launch_template_version=launch_template_version,
            launch_template_id=launch_template_id,
            x_region=x_region,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout
        )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x-region": x_region}), **(extra_headers or {})}
        network_id = self._fetch_network_id_from_vpc(
            vpc_krn=vpc_krn,
            vpc_name=vpc_name,
            x_region=x_region,
            extra_headers=extra_headers,
            timeout=timeout,
        )
        return self._post(
            "/asg/v1",
            body=maybe_transform(
                {
                    "asg_name": asg_name,
                    "attach_floating_ip": False,
                    "image_krn": image_krn,
                    "instance_name": instance_name,
                    "instanceType": instance_type,
                    "max": max,
                    "min": min,
                    "network_krn": network_id,
                    "policy": policy,
                    "region": region,
                    "save_as_template": save_as_template,
                    "security_groups": security_groups,
                    "sshkey_name": sshkey_name,
                    "subnet_id": subnet_id,
                    "tags": [],
                    "volume_name": volume_name,
                    "volume_size": volume_size,
                    "user_data": user_data,
                    "vpc_krn": vpc_krn,
                    "launch_from_template": launch_from_template,
                    "volumeType": volume_type,
                    "launch_template_id": launch_template_id,
                    "launch_template_version": launch_template_version,
                },
                v1_create_asg_params.V1CreateAsgParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def create_launch_template(
        self,
        *,
        image_krn: str | Omit = omit,
        user_data: str | NotGiven = NOT_GIVEN,
        instance_name: str | Omit = omit,
        instance_type: str | Omit = omit,
        max: int | Omit = omit,
        min: int | Omit = omit,
        vpc_name: str | Omit = omit,
        policy: Iterable[PolicyParam] | NotGiven = NOT_GIVEN,
        region: str | Omit = omit,
        security_groups: SequenceNotStr[str] | Omit = omit,
        sshkey_name: str | Omit = omit,
        subnet_id: str | Omit = omit,
        template_name: str | Omit = omit,
        volume_name: str | Omit = omit,
        volume_size: Iterable[VolumeParam],
        volume_type: str,
        vpc_krn: str | Omit = omit,
        x_region: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Launch Template

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """


        self.validate_create_launch_template_parameters(
            image_krn=image_krn,
            instance_name=instance_name,
            instance_type=instance_type,
            max=max,
            min=min,
            vpc_name=vpc_name,
            region=region,
            security_groups=security_groups,
            sshkey_name=sshkey_name,
            subnet_id=subnet_id,
            template_name=template_name,
            volume_size=volume_size,
            volume_name=volume_name,
            volume_type=volume_type,
            vpc_krn=vpc_krn,
            x_region=x_region,
            user_data=user_data,
            policy=policy,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout
        )

        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x_region": x_region}), **(extra_headers or {})}
        network_id = self._fetch_network_id_from_vpc(
            vpc_krn=vpc_krn,
            vpc_name=vpc_name,
            x_region=x_region,
            extra_headers=extra_headers,
            timeout=timeout,
        )
        return self._post(
            "/asg/v1/create-launch-template",
            body=maybe_transform(
                {
                    "image_krn": image_krn,
                    "instance_name": instance_name,
                    "instance_type": instance_type,
                    "max": max,
                    "min": min,
                    "network_krn": network_id,
                    "policy": policy,
                    "qos": {
                        "iops": {},
                        "bandwidth": {}
                    },
                    "attach_floating_ip": False,
                    "region": region,
                    "security_groups": security_groups,
                    "sshkey_name": sshkey_name,
                    "subnet_id": subnet_id,
                    "template_name": template_name,
                    "volume_name": volume_name,
                    "volume_size": volume_size,
                    "volume_type": volume_type,
                    "user_data": user_data,
                    "vpc_krn": vpc_krn,
                },
                v1_create_launch_template_params.V1CreateLaunchTemplateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def delete_asg(
        self,
        asg_krn: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete ASG

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not asg_krn:
            raise ValueError(f"Expected a non-empty value for `asg_krn` but received {asg_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/asg/v1/delete_asg/{asg_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def delete_launch_template(
        self,
        *,
        template_id: str,
        template_name: str,
        version: int,
        x_region: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Launch Template

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region})
        return self._post(
            "/asg/v1/delete-launch-template",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "template_id": template_id,
                        "template_name": template_name,
                        "version": version,
                    },
                    v1_delete_launch_template_params.V1DeleteLaunchTemplateParams,
                ),
            ),
            cast_to=NoneType,
        )

    def downscale_asg(
        self,
        *,
        asg_krn: str | Omit = omit,
        count: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Downscale ASG

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/asg/v1/downscale",
            body=maybe_transform(
                {
                    "asg_krn": asg_krn,
                    "count": count,
                },
                v1_downscale_asg_params.V1DownscaleAsgParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get_launch_templates(
        self,
        *,
        page: int,
        size: int,
        vpc_id: str,
        x_region: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get Launch Templates

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x-region": x_region}), **(extra_headers or {})}
        return self._get(
            "/asg/v1/get-launch-template",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "size": size,
                        "vpc_id": vpc_id,
                    },
                    v1_get_launch_templates_params.V1GetLaunchTemplatesParams,
                ),
            ),
            cast_to=NoneType,
        )

    def retrieve_asg(
        self,
        *,
        page: int,
        size: int,
        asg_krn: str | Omit = omit,
        asg_name: str | Omit = omit,
        x_region: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Retrieve ASG

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x-region": x_region}), **(extra_headers or {})}
        return self._get(
            "/asg/v1/retrieve_asg",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "size": size,
                        "asg_krn": asg_krn,
                        "asg_name": asg_name,
                    },
                    v1_retrieve_asg_params.V1RetrieveAsgParams,
                ),
            ),
            cast_to=NoneType,
        )

    def update_asg(
        self,
        *,
        asg_krn: str | Omit = omit,
        instance_type: str | NotGiven = NOT_GIVEN,
        max: int | NotGiven = NOT_GIVEN,
        min: int | NotGiven = NOT_GIVEN,
        policy: Iterable[PolicyParam] | NotGiven = NOT_GIVEN,
        security_groups: SequenceNotStr[str] | NotGiven = NOT_GIVEN,
        sshkey_name: str | NotGiven = NOT_GIVEN,
        volume_size: Iterable[VolumeParam] | NotGiven = NOT_GIVEN,
        volume_name: str | NotGiven = NOT_GIVEN,
        user_data: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Update Auto Scaling Group

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """

        self.validate_update_asg_parameters(
            asg_krn=asg_krn,
            instance_type=instance_type,
            max=max,
            min=min,
            policy=policy,
            security_groups=security_groups,
            sshkey_name=sshkey_name,
            volume_name=volume_name,
            volume_size=volume_size,
            user_data=user_data,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout
        )

        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/asg/v1/update_asg",
            body=maybe_transform(
                {
                    "asg_krn": asg_krn,
                    "instance_type": instance_type,
                    "max": max,
                    "min": min,
                    "policy": policy,
                    "security_groups": security_groups,
                    "sshkey_name": sshkey_name,
                    "volumeName": volume_name,
                    "tags": [],
                    "volume_size": volume_size,
                    "user_data": user_data,
                },
                v1_update_asg_params.V1UpdateAsgParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def update_launch_template(
        self,
        *,
        template_id: str,
        template_name: str,
        instance_name: str | Omit = omit,
        instance_type: str | Omit = omit,
        sshkey_name: str | Omit = omit,
        image_krn: str | Omit = omit,
        security_groups: Iterable[str] | Omit = omit,
        min: int | Omit = omit,
        max: int | Omit = omit,
        volume_size: Iterable[VolumeParam] | Omit = omit,
        policy: Iterable[PolicyParam] | NotGiven = NOT_GIVEN,
        volume_name: str | NotGiven = NOT_GIVEN,
        volume_type: str | NotGiven = NOT_GIVEN,
        user_data: str | NotGiven = NOT_GIVEN,
        x_region: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Update Launch Template

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_update_launch_template_parameters(
            template_id=template_id,
            template_name=template_name,
            instance_name=instance_name,
            instance_type=instance_type,
            sshkey_name=sshkey_name,
            image_krn=image_krn,
            security_groups=security_groups,
            min=min,
            max=max,
            volume_size=volume_size,
            policy=policy,
            volume_name=volume_name,
            volume_type=volume_type,
            user_data=user_data,
            x_region=x_region,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout
        )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x_region": x_region}), **(extra_headers or {})}
        breakpoint()
        print(policy)
        return self._post(
            "/asg/v1/update-launch-template",
            body=maybe_transform(
                {
                    "policy": policy,
                    "qos": {
                        "iops": {},
                        "bandwidth": {}
                    },
                    "volume_size": volume_size,
                    "volumeName": volume_name,
                    "volumeType": volume_type,
                    "instanceName": instance_name,
                    "instanceType": instance_type,
                    "sshkey_name": sshkey_name,
                    "user_data": user_data,
                    "image_krn": image_krn,
                    "security_groups":security_groups,
                    "min": min,
                    "max": max
                },
                v1_update_launch_template_params.V1UpdateLaunchTemplateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "template_id": template_id,
                        "template_name": template_name,
                    },
                    v1_update_launch_template_params.V1UpdateLaunchTemplateParams,
                ),
            ),
            cast_to=NoneType,
        )

    def upscale_asg(
        self,
        *,
        asg_krn: str | Omit = omit,
        desired_vm_count: int | Omit = omit,
        vpc_krn: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Upscale ASG

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/asg/v1/upscale",
            body=maybe_transform(
                {
                    "asg_krn": asg_krn,
                    "attach_floating_ip": False,
                    "desired_vm_count": desired_vm_count,
                    "vpc_krn": vpc_krn,
                },
                v1_upscale_asg_params.V1UpscaleAsgParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncV1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/asg-python#accessing-raw-response-data-eg-headers
        """
        return AsyncV1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncV1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/asg-python#with_streaming_response
        """
        return AsyncV1ResourceWithStreamingResponse(self)
    


    def validate_create_launch_template_parameters(
        self,
        image_krn,
        instance_name,
        instance_type,
        max,
        min,
        vpc_name,
        region,
        security_groups,
        sshkey_name,
        subnet_id,
        template_name,
        volume_size,
        volume_name,
        volume_type,
        vpc_krn,
        x_region,
        user_data=None,
        policy=None,
        extra_headers=None,
        extra_query=None,
        extra_body=None,
        timeout=None,
    ):
        # 1. Validate String parameters (Non-empty if not omitted)
        for name, value in {
            "image_krn": image_krn,
            "instance_name": instance_name,
            "instance_type": instance_type,
            "network_krn": vpc_name,
            "region": region,
            "sshkey_name": sshkey_name,
            "subnet_id": subnet_id,
            "template_name": template_name,
            "vpc_krn": vpc_krn,
            "volume_name": volume_name,
            "volume_type":volume_type
        }.items():
            if value is not omit:
                if not isinstance(value, str) or not value:
                    raise ValueError(f"'{name}' must be a non-empty string.")

        # 2. Validate Integers
        for name, value in {"min": min, "max": max}.items():
            if value is not omit and not isinstance(value, int):
                raise ValueError(f"'{name}' must be an integer.")

        # 3. Validate Iterables
        if security_groups is not omit and not isinstance(security_groups, (list, tuple)):
            raise ValueError("'security_groups' must be a list or tuple.")
        
        # volume_size is mandatory in your signature
        if not isinstance(volume_size, (list, tuple, Iterable)):
            raise ValueError("'volume_size' must be an iterable of VolumeParam.")

        # 5. Optional Parameters (user_data and policy)
        if user_data not in (None, NOT_GIVEN):
            if not isinstance(user_data, (str, dict)):
                raise ValueError("'user_data' must be a string or dictionary if provided.")

        if policy not in (None, NOT_GIVEN):
            if not isinstance(policy, (list, tuple, Iterable)):
                raise ValueError("'policy' must be an iterable of PolicyParam if provided.")

        # 6. Extra Dicts & Timeout
        if extra_headers is not None and not isinstance(extra_headers, dict):
            raise ValueError("'extra_headers' must be a dictionary.")
        if extra_query is not None and not isinstance(extra_query, dict):
            raise ValueError("'extra_query' must be a dictionary.")
        if extra_body is not None and not isinstance(extra_body, dict):
            raise ValueError("'extra_body' must be a dictionary.")

        if timeout not in (None, NOT_GIVEN) and not isinstance(timeout, (int, float, httpx.Timeout)):
            raise ValueError("'timeout' must be a float, int, or httpx.Timeout.")

        # 7. Literal Constraints
        if x_region is not omit and x_region not in ("In-Bangalore-1"):
            raise ValueError("'x_region' must be 'In-Bangalore-1'")
        

    def _fetch_network_id_from_vpc(
        self,
        *,
        vpc_krn: str,
        vpc_name: str,
        x_region: str | None,
        extra_headers: Headers | None,
        timeout: float | httpx.Timeout | None | NotGiven,
    ) -> str:
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x-region": x_region}), **extra_headers}

        api_response = self._get(
            "/v1/highlvlvpc/describe_vpc",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query={
                    "vpc_name": vpc_name,
                    "vpc_id": vpc_krn,
                },
                timeout=timeout,
            ),
            cast_to=dict,
        )

        data = api_response.json()

        vpc_data = next(iter(data.values()))

        return vpc_data["networks"]["krn_id"]
        

    def validate_create_asg_parameters(
        self,
        asg_name,
        image_krn,
        instance_name,
        subnet_id,
        max,
        min,
        save_as_template,
        vpc_krn,
        vpc_name,
        x_region,
        launch_from_template,
        instance_type=None,
        policy=None,
        region=None,
        security_groups=None,
        sshkey_name=None,
        volume_name=None,
        volume_size=None,
        volume_type=None,
        launch_template_version=None,
        launch_template_id=None,
        user_data=None,
        extra_headers=None,
        extra_query=None,
        extra_body=None,
        timeout=None,
    ):
        # 1. Mandatory/Omit-aware String Validation
        for name, value in {
            "asg_name": asg_name,
            "image_krn": image_krn,
            "instance_name": instance_name,
            "subnet_id": subnet_id,
            "vpc_krn": vpc_krn,
            "vpc_name": vpc_name
        }.items():
            if value is not omit:
                if not isinstance(value, str) or not value:
                    raise ValueError(f"'{name}' must be a non-empty string.")

        # 2. Optional String Validation (Fields that default to None)
        optional_strings = {
            "instance_type": instance_type,
            "region": region,
            "sshkey_name": sshkey_name,
            "volume_name": volume_name,
            "volume_type": volume_type,
            "launch_template_id": launch_template_id
        }
        for name, value in optional_strings.items():
            if value not in (None, omit, NOT_GIVEN):
                if not isinstance(value, str) or not value:
                    raise ValueError(f"'{name}' must be a non-empty string if provided.")

        # 3. Validate Booleans
        for name, value in {
            "save_as_template": save_as_template,
            "launch_from_template": launch_from_template,
        }.items():
            if value is not omit and not isinstance(value, bool):
                raise ValueError(f"'{name}' must be a boolean if provided.")

        # 4. Validate Integers
        # Added launch_template_version to integer check
        for name, value in {
            "min": min, 
            "max": max, 
            "launch_template_version": launch_template_version
        }.items():
            if value not in (None, omit, NOT_GIVEN) and not isinstance(value, int):
                raise ValueError(f"'{name}' must be an integer if provided.")

        # 5. Validate Iterables / Sequences
        if policy not in (None, omit, NOT_GIVEN) and not isinstance(policy, (list, tuple, Iterable)):
            raise ValueError("'policy' must be an iterable in the correct format.")

        if security_groups not in (None, omit, NOT_GIVEN) and not isinstance(security_groups, (list, tuple, Sequence)):
            raise ValueError("'security_groups' must be a sequence of strings.")

        if volume_size not in (None, omit, NOT_GIVEN) and not isinstance(volume_size, (list, tuple, Iterable)):
            raise ValueError("'volume_size' must be an iterable in the correct format.")

        # 6. Optional: user_data
        if user_data not in (None, omit, NOT_GIVEN):
            if not isinstance(user_data, (str, dict)):
                raise ValueError("'user_data' must be a string or dictionary if provided.")

        # 7. Optional: extra dicts & timeout
        if extra_headers is not None and not isinstance(extra_headers, dict):
            raise ValueError("'extra_headers' must be a dictionary if provided.")
        if extra_query is not None and not isinstance(extra_query, dict):
            raise ValueError("'extra_query' must be a dictionary if provided.")
        if extra_body is not None and not isinstance(extra_body, dict):
            raise ValueError("'extra_body' must be a dictionary if provided.")

        if timeout not in (None, NOT_GIVEN) and not isinstance(timeout, (int, float, httpx.Timeout)):
            raise ValueError("'timeout' must be a float, int, or httpx.Timeout if provided.")

        # 8. Literal Constraints for x_region
        if x_region is omit or x_region is None:
            raise ValueError("'x_region' is required.")
        
        if x_region != "In-Bangalore-1":
            raise ValueError("'x_region' must be 'In-Bangalore-1'.")
        


    def validate_update_asg_parameters(
        self,
        asg_krn,
        instance_type=None,
        max=None,
        min=None,
        policy=None,
        security_groups=None,
        sshkey_name=None,
        volume_size=None,
        volume_name=None,
        user_data=None,
        extra_headers=None,
        extra_query=None,
        extra_body=None,
        timeout=None,
    ):
    # 1. Mandatory-if-provided Strings (asg_krn, image_krn, instance_type, etc.)
    # We use a tuple for the skip condition to catch all 'empty' states
        skip_conditions = (None, omit, NOT_GIVEN)

        for name, value in {
            "asg_krn": asg_krn,
            "instance_type": instance_type,
            "sshkey_name": sshkey_name,
            "volume_name": volume_name,
        }.items():
            if value not in skip_conditions:
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"'{name}' must be a non-empty string if provided.")

        # 2. Validate Integers (min/max)
        for name, value in {"min": min, "max": max}.items():
            if value not in skip_conditions:
                if not isinstance(value, int):
                    raise ValueError(f"'{name}' must be an integer if provided.")

        # 3. Validate Iterables / Sequences
        iterable_checks = [
            ("policy", policy, (list, tuple, Iterable)),
            ("security_groups", security_groups, (list, tuple, Sequence)),
            ("volume_size", volume_size, (list, tuple, Iterable))
        ]
        for name, value, expected_types in iterable_checks:
            if value not in skip_conditions:
                if not isinstance(value, expected_types):
                    raise ValueError(f"'{name}' must be an iterable in the correct format.")

        # 4. Optional: user_data (string or dict)
        if user_data not in skip_conditions:
            if not isinstance(user_data, (str, dict)):
                raise ValueError("'user_data' must be a string or dictionary if provided.")

        # 5. Optional: extra dicts & timeout
        for name, value in {
            "extra_headers": extra_headers,
            "extra_query": extra_query,
            "extra_body": extra_body
        }.items():
            if value is not None and not isinstance(value, dict):
                raise ValueError(f"'{name}' must be a dictionary if provided.")

        if timeout not in (None, NOT_GIVEN) and not isinstance(timeout, (int, float, httpx.Timeout)):
            raise ValueError("'timeout' must be a float, int, or httpx.Timeout if provided.")



            

    async def create_asg(
        self,
        *,
        asg_name: str | Omit = omit,
        vpc_name: str | Omit = omit,
        image_krn: str | Omit = omit,
        instance_name: str | Omit = omit,
        instance_type: str | NotGiven = NOT_GIVEN,
        max: int | Omit = omit,
        min: int | Omit = omit,
        policy: Iterable[PolicyParam] | NotGiven = NOT_GIVEN,
        region: str | NotGiven = NOT_GIVEN,
        save_as_template: bool | Omit = omit,
        security_groups: SequenceNotStr[str] |  NotGiven = NOT_GIVEN,
        sshkey_name: str |  NotGiven = NOT_GIVEN,
        subnet_id: str | Omit = omit,
        volume_name: str | NotGiven = NOT_GIVEN,
        volume_size: Iterable[VolumeParam] | NotGiven = NOT_GIVEN,
        volume_type: str | NotGiven = NOT_GIVEN,
        user_data: str | NotGiven = NOT_GIVEN,
        launch_template_id: str | NotGiven = NOT_GIVEN,
        launch_template_version: int | NotGiven = NOT_GIVEN,
        vpc_krn: str | Omit = omit,
        launch_from_template: bool | Omit = omit,
        x_region: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Auto Scaling Group

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        
        self.validate_create_asg_parameters(
            asg_name=asg_name,
            image_krn=image_krn,
            instance_name=instance_name,
            instance_type=instance_type,
            max=max,
            min=min,
            region=region,
            save_as_template=save_as_template,
            security_groups=security_groups,
            sshkey_name=sshkey_name,
            subnet_id=subnet_id,
            volume_name=volume_name,
            volume_size=volume_size,
            volume_type=volume_type,
            policy=policy,
            vpc_krn=vpc_krn,
            vpc_name=vpc_name,
            launch_from_template=launch_from_template,
            user_data=user_data,
            launch_template_version=launch_template_version,
            launch_template_id=launch_template_id,
            x_region=x_region,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout
        )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x-region": x_region}), **(extra_headers or {})}
        network_id = self._fetch_network_id_from_vpc(
            vpc_krn=vpc_krn,
            vpc_name=vpc_name,
            x_region=x_region,
            extra_headers=extra_headers,
            timeout=timeout,
        )
        return await self._post(
            "/asg/v1",
            body= await async_maybe_transform(
                {
                    "asg_name": asg_name,
                    "attach_floating_ip": False,
                    "image_krn": image_krn,
                    "instance_name": instance_name,
                    "instanceType": instance_type,
                    "max": max,
                    "min": min,
                    "network_krn": network_id,
                    "policy": policy,
                    "region": region,
                    "save_as_template": save_as_template,
                    "security_groups": security_groups,
                    "sshkey_name": sshkey_name,
                    "subnet_id": subnet_id,
                    "tags": [],
                    "volume_name": volume_name,
                    "volume_size": volume_size,
                    "user_data": user_data,
                    "vpc_krn": vpc_krn,
                    "launch_from_template": launch_from_template,
                    "volumeType": volume_type,
                    "launch_template_id": launch_template_id,
                    "launch_template_version": launch_template_version,
                },
                v1_create_asg_params.V1CreateAsgParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )
    async def create_launch_template(
        self,
        *,
        image_krn: str | Omit = omit,
        user_data: str | NotGiven = NOT_GIVEN,
        instance_name: str | Omit = omit,
        instance_type: str | Omit = omit,
        max: int | Omit = omit,
        min: int | Omit = omit,
        vpc_name: str | Omit = omit,
        policy: Iterable[PolicyParam] | NotGiven = NOT_GIVEN,
        region: str | Omit = omit,
        security_groups: SequenceNotStr[str] | Omit = omit,
        sshkey_name: str | Omit = omit,
        subnet_id: str | Omit = omit,
        template_name: str | Omit = omit,
        volume_name: str | Omit = omit,
        volume_size: Iterable[VolumeParam],
        volume_type: str,
        vpc_krn: str | Omit = omit,
        x_region: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create Launch Template

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """


        self.validate_create_launch_template_parameters(
            image_krn=image_krn,
            instance_name=instance_name,
            instance_type=instance_type,
            max=max,
            min=min,
            vpc_name=vpc_name,
            region=region,
            security_groups=security_groups,
            sshkey_name=sshkey_name,
            subnet_id=subnet_id,
            template_name=template_name,
            volume_size=volume_size,
            volume_name=volume_name,
            volume_type=volume_type,
            vpc_krn=vpc_krn,
            x_region=x_region,
            user_data=user_data,
            policy=policy,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout
        )

        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x_region": x_region}), **(extra_headers or {})}
        network_id = self._fetch_network_id_from_vpc(
            vpc_krn=vpc_krn,
            vpc_name=vpc_name,
            x_region=x_region,
            extra_headers=extra_headers,
            timeout=timeout,
        )
        return await self._post(
            "/asg/v1/create-launch-template",
            body=await async_maybe_transform(
                {
                    "image_krn": image_krn,
                    "instance_name": instance_name,
                    "instance_type": instance_type,
                    "max": max,
                    "min": min,
                    "network_krn": network_id,
                    "policy": policy,
                    "qos": {
                        "iops": {},
                        "bandwidth": {}
                    },
                    "attach_floating_ip": False,
                    "region": region,
                    "security_groups": security_groups,
                    "sshkey_name": sshkey_name,
                    "subnet_id": subnet_id,
                    "template_name": template_name,
                    "volume_name": volume_name,
                    "volume_size": volume_size,
                    "volume_type": volume_type,
                    "user_data": user_data,
                    "vpc_krn": vpc_krn,
                },
                v1_create_launch_template_params.V1CreateLaunchTemplateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )
    


    async def delete_asg(
        self,
        asg_krn: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete ASG

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not asg_krn:
            raise ValueError(f"Expected a non-empty value for `asg_krn` but received {asg_krn!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/asg/v1/delete_asg/{asg_krn}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def delete_launch_template(
        self,
        *,
        template_id: str,
        template_name: str,
        version: int,
        x_region: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Launch Template

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"x-region": x_region})
        return await self._post(
            "/asg/v1/delete-launch-template",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "template_id": template_id,
                        "template_name": template_name,
                        "version": version,
                    },
                    v1_delete_launch_template_params.V1DeleteLaunchTemplateParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def downscale_asg(
        self,
        *,
        asg_krn: str | Omit = omit,
        count: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Downscale ASG

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/asg/v1/downscale",
            body=await async_maybe_transform(
                {
                    "asg_krn": asg_krn,
                    "count": count,
                },
                v1_downscale_asg_params.V1DownscaleAsgParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_launch_templates(
        self,
        *,
        page: int,
        size: int,
        vpc_id: str,
        x_region: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Get Launch Templates

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x-region": x_region}), **(extra_headers or {})}
        return await self._get(
            "/asg/v1/get-launch-template",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "page": page,
                        "size": size,
                        "vpc_id": vpc_id,
                    },
                    v1_get_launch_templates_params.V1GetLaunchTemplatesParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def retrieve_asg(
        self,
        *,
        page: int,
        size: int,
        asg_krn: str | Omit = omit,
        asg_name: str | Omit = omit,
        x_region: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Retrieve ASG

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x-region": x_region}), **(extra_headers or {})}
        return await self._get(
            "/asg/v1/retrieve_asg",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "page": page,
                        "size": size,
                        "asg_krn": asg_krn,
                        "asg_name": asg_name,
                    },
                    v1_retrieve_asg_params.V1RetrieveAsgParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def update_asg(
        self,
        *,
        asg_krn: str | Omit = omit,
        instance_type: str | NotGiven = NOT_GIVEN,
        max: int | NotGiven = NOT_GIVEN,
        min: int | NotGiven = NOT_GIVEN,
        policy: Iterable[PolicyParam] | NotGiven = NOT_GIVEN,
        security_groups: SequenceNotStr[str] | NotGiven = NOT_GIVEN,
        sshkey_name: str | NotGiven = NOT_GIVEN,
        volume_size: Iterable[VolumeParam] | NotGiven = NOT_GIVEN,
        volume_name: str | NotGiven = NOT_GIVEN,
        user_data: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Update Auto Scaling Group

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """

        self.validate_update_asg_parameters(
            asg_krn=asg_krn,
            instance_type=instance_type,
            max=max,
            min=min,
            policy=policy,
            security_groups=security_groups,
            sshkey_name=sshkey_name,
            volume_name=volume_name,
            volume_size=volume_size,
            user_data=user_data,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout
        )

        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/asg/v1/update_asg",
            body=await async_maybe_transform(
                {
                    "asg_krn": asg_krn,
                    "instance_type": instance_type,
                    "max": max,
                    "min": min,
                    "policy": policy,
                    "security_groups": security_groups,
                    "sshkey_name": sshkey_name,
                    "volumeName": volume_name,
                    "tags": [],
                    "volume_size": volume_size,
                    "user_data": user_data,
                },
                v1_update_asg_params.V1UpdateAsgParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


    async def update_launch_template(
        self,
        *,
        template_id: str,
        template_name: str,
        instance_name: str | Omit = omit,
        instance_type: str | Omit = omit,
        sshkey_name: str | Omit = omit,
        image_krn: str | Omit = omit,
        security_groups: Iterable[str] | Omit = omit,
        min: int | Omit = omit,
        max: int | Omit = omit,
        volume_size: Iterable[VolumeParam] | Omit = omit,
        policy: Iterable[PolicyParam] | NotGiven = NOT_GIVEN,
        volume_name: str | NotGiven = NOT_GIVEN,
        volume_type: str | NotGiven = NOT_GIVEN,
        user_data: str | NotGiven = NOT_GIVEN,
        x_region: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Update Launch Template

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        self.validate_update_launch_template_parameters(
            template_id=template_id,
            template_name=template_name,
            instance_name=instance_name,
            instance_type=instance_type,
            sshkey_name=sshkey_name,
            image_krn=image_krn,
            security_groups=security_groups,
            min=min,
            max=max,
            volume_size=volume_size,
            policy=policy,
            volume_name=volume_name,
            volume_type=volume_type,
            user_data=user_data,
            x_region=x_region,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout
        )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers = {**strip_not_given({"x_region": x_region}), **(extra_headers or {})}
        return await self._post(
            "/asg/v1/update-launch-template",
            body=await async_maybe_transform(
                {
                    "policy": policy,
                    "qos": {
                        "iops": {},
                        "bandwidth": {}
                    },
                    "volume_size": volume_size,
                    "volumeName": volume_name,
                    "volumeType": volume_type,
                    "instanceName": instance_name,
                    "instanceType": instance_type,
                    "sshkey_name": sshkey_name,
                    "user_data": user_data,
                    "image_krn": image_krn,
                    "security_groups":security_groups,
                    "min": min,
                    "max": max
                },
                v1_update_launch_template_params.V1UpdateLaunchTemplateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "template_id": template_id,
                        "template_name": template_name,
                    },
                    v1_update_launch_template_params.V1UpdateLaunchTemplateParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def upscale_asg(
        self,
        *,
        asg_krn: str | Omit = omit,
        desired_vm_count: int | Omit = omit,
        vpc_krn: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Upscale ASG

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/asg/v1/upscale",
            body=await async_maybe_transform(
                {
                    "asg_krn": asg_krn,
                    "attach_floating_ip": False,
                    "desired_vm_count": desired_vm_count,
                    "vpc_krn": vpc_krn,
                },
                v1_upscale_asg_params.V1UpscaleAsgParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.create_asg = to_raw_response_wrapper(
            v1.create_asg,
        )
        self.create_launch_template = to_raw_response_wrapper(
            v1.create_launch_template,
        )
        self.delete_asg = to_raw_response_wrapper(
            v1.delete_asg,
        )
        self.delete_launch_template = to_raw_response_wrapper(
            v1.delete_launch_template,
        )
        self.downscale_asg = to_raw_response_wrapper(
            v1.downscale_asg,
        )
        self.get_launch_templates = to_raw_response_wrapper(
            v1.get_launch_templates,
        )
        self.retrieve_asg = to_raw_response_wrapper(
            v1.retrieve_asg,
        )
        self.update_asg = to_raw_response_wrapper(
            v1.update_asg,
        )
        self.update_launch_template = to_raw_response_wrapper(
            v1.update_launch_template,
        )
        self.upscale_asg = to_raw_response_wrapper(
            v1.upscale_asg,
        )


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.create_asg = async_to_raw_response_wrapper(
            v1.create_asg,
        )
        self.create_launch_template = async_to_raw_response_wrapper(
            v1.create_launch_template,
        )
        self.delete_asg = async_to_raw_response_wrapper(
            v1.delete_asg,
        )
        self.delete_launch_template = async_to_raw_response_wrapper(
            v1.delete_launch_template,
        )
        self.downscale_asg = async_to_raw_response_wrapper(
            v1.downscale_asg,
        )
        self.get_launch_templates = async_to_raw_response_wrapper(
            v1.get_launch_templates,
        )
        self.retrieve_asg = async_to_raw_response_wrapper(
            v1.retrieve_asg,
        )
        self.update_asg = async_to_raw_response_wrapper(
            v1.update_asg,
        )
        self.update_launch_template = async_to_raw_response_wrapper(
            v1.update_launch_template,
        )
        self.upscale_asg = async_to_raw_response_wrapper(
            v1.upscale_asg,
        )


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.create_asg = to_streamed_response_wrapper(
            v1.create_asg,
        )
        self.create_launch_template = to_streamed_response_wrapper(
            v1.create_launch_template,
        )
        self.delete_asg = to_streamed_response_wrapper(
            v1.delete_asg,
        )
        self.delete_launch_template = to_streamed_response_wrapper(
            v1.delete_launch_template,
        )
        self.downscale_asg = to_streamed_response_wrapper(
            v1.downscale_asg,
        )
        self.get_launch_templates = to_streamed_response_wrapper(
            v1.get_launch_templates,
        )
        self.retrieve_asg = to_streamed_response_wrapper(
            v1.retrieve_asg,
        )
        self.update_asg = to_streamed_response_wrapper(
            v1.update_asg,
        )
        self.update_launch_template = to_streamed_response_wrapper(
            v1.update_launch_template,
        )
        self.upscale_asg = to_streamed_response_wrapper(
            v1.upscale_asg,
        )


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.create_asg = async_to_streamed_response_wrapper(
            v1.create_asg,
        )
        self.create_launch_template = async_to_streamed_response_wrapper(
            v1.create_launch_template,
        )
        self.delete_asg = async_to_streamed_response_wrapper(
            v1.delete_asg,
        )
        self.delete_launch_template = async_to_streamed_response_wrapper(
            v1.delete_launch_template,
        )
        self.downscale_asg = async_to_streamed_response_wrapper(
            v1.downscale_asg,
        )
        self.get_launch_templates = async_to_streamed_response_wrapper(
            v1.get_launch_templates,
        )
        self.retrieve_asg = async_to_streamed_response_wrapper(
            v1.retrieve_asg,
        )
        self.update_asg = async_to_streamed_response_wrapper(
            v1.update_asg,
        )
        self.update_launch_template = async_to_streamed_response_wrapper(
            v1.update_launch_template,
        )
        self.upscale_asg = async_to_streamed_response_wrapper(
            v1.upscale_asg,
        )