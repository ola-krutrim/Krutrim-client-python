from __future__ import annotations

import os
from typing import Any

import httpx

from ..._types import NOT_GIVEN, Headers, NoneType, NotGiven, Query
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options


__all__ = [
    "IAMResource",
    "AsyncIAMResource",
    "IAMResourceWithRawResponse",
    "AsyncIAMResourceWithRawResponse",
    "IAMResourceWithStreamingResponse",
    "AsyncIAMResourceWithStreamingResponse",
]


# =========================
# SYNC RESOURCE
# =========================
class IAMResource(SyncAPIResource):

    @cached_property
    def with_raw_response(self) -> "IAMResourceWithRawResponse":
        return IAMResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> "IAMResourceWithStreamingResponse":
        return IAMResourceWithStreamingResponse(self)


    def _auth_headers(self, extra_headers: Headers | None = None) -> Headers:
        headers = {"Accept": "*/*", **(extra_headers or {})}

        token = getattr(self._client, "token", None) or getattr(self._client, "api_key", None)
        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    # -------------------------
    # CREATE USER (NO AUTH)
    # -------------------------
    def create_user(
        self,
        *,
        user_name: str,
        email: str,
        password: str,
        console_access: bool,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:

        headers = {"Accept": "*/*", **(extra_headers or {})}

        return self._post(
            "/iam/v1/user",
            body={
                "user": {
                    "userName": user_name,
                    "email": email,
                    "password": password,
                    "consoleAccess": console_access,
                }
            },
            options=make_request_options(
                extra_headers=headers,
                timeout=timeout,
            ),
            cast_to=object,
        )

    # -------------------------
    # ENABLE PROGRAMMATIC ACCESS
    # -------------------------
    def enable_programmatic_access(
        self,
        user_krn: str,
        *,

        extra_headers: Headers | None = None,
    ) -> object:

        if not user_krn:
            raise ValueError("Expected non-empty user_krn")

        headers = self._auth_headers(extra_headers)


        return self._post(
            f"/iam/v1/users/programmaticAccess/{user_krn}",
            body={},
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )

    # -------------------------
    # LIST ROLES
    # -------------------------
    def list_roles(
        self,
        *,

        limit: int = 9999,
        offset: int = 0,
        krutrim_managed: bool | str | None = None,
        krutrimManaged: bool | str | None = None,
        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)

        managed = krutrimManaged if krutrimManaged is not None else krutrim_managed
        if managed is None:
            managed_value = "all"
        elif isinstance(managed, bool):
            managed_value = "true" if managed else "false"
        else:
            managed_value = str(managed).lower()


        return self._get(
            "/iam/v1/roles",
            options=make_request_options(
                extra_headers=headers,
                query={
                    "limit": limit,
                    "offset": offset,
                    "krutrimManaged": managed_value,
                },
            ),
            cast_to=object,
        )

    # -------------------------
    # SIGNIN PROGRAMMATIC USER
    # -------------------------
    def signin_programmatic_user(
        self,
        *,
        account_id: str,
        access_key: str,
        secret_key: str,
        extra_headers: Headers | None = None,
    ) -> object:

        headers = {"Content-Type": "application/json", **(extra_headers or {})}

        resp = self._post(
            "/iam/v1/signinProgrammaticUser",
            body={
                "accountId": account_id,
                "accessKey": access_key,
                "secretKey": secret_key,
            },
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )


        if isinstance(resp, dict):
            token = resp.get("token") or resp.get("access_token")
            if token:
                self._client.api_key = token
                setattr(self._client, "token", token)

        return resp

    # -------------------------
    # SIGN IN AS ROOT USER
    # -------------------------
    def sign_in_as_root_user(
        self,
        *,
        email: str,
        password: str,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        headers = {"Content-Type": "application/json", **(extra_headers or {})}

        resp = self._post(
            "/iam/v1/signInAsRootUser",
            body={
                "email": email,
                "password": password,
            },
            options=make_request_options(
                extra_headers=headers,
                timeout=timeout,
            ),
            cast_to=object,
        )

        if isinstance(resp, dict):
            token = resp.get("access_token") or resp.get("token")
            if token:
                self._client.api_key = token
                setattr(self._client, "token", token)

        return resp

    def get_role(
        self,
        role_krn: str,
        *,

        extra_headers: Headers | None = None,
    ) -> object:

        if not role_krn:
            raise ValueError("Expected non-empty role_krn")

        headers = self._auth_headers(extra_headers)


        return self._get(
            f"/iam/v1/roles/{role_krn}",
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )
    
    def delete_role(
        self,
        role_krn: str,
        *,

        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)


        return self._delete(
            f"/iam/v1/roles/{role_krn}",
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )
    def attach_policies_to_role(
        self,
        *,
        role_id: str,
        policy_ids: list[str],

        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)


        return self._put(
            "/iam/v1/urgp/role/policy",
            body={
                "roleId": role_id,
                "policyIds": policy_ids,
            },
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )
    
    def reset_programmatic_access(
        self,
        user_krn: str,
        *,

        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)


        return self._post(
            f"/iam/v1/users/resetProgrammaticAccess/{user_krn}",
            body={},
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )
    def disable_programmatic_access(
        self,
        user_krn: str,
        *,
        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)


        return self._put(
            f"/iam/v1/users/disableProgrammaticAccess/{user_krn}",
            body={},
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )
    def list_policies(
        self,
        *,

        limit: int = 10,
        offset: int = 0,
        krutrim_managed: str = "all", 
        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)


        return self._get(
            "/iam/v1/policies",
            options=make_request_options(
                extra_headers=headers,
                query={
                    "limit": limit,
                    "offset": offset,
                    "krutrimManaged": str(krutrim_managed).lower(),  # true/false
                },
            ),
            cast_to=object,
        )
    def assign_roles_to_user(
        self,
        *,
        user_id: str,
        role_ids: list[str],
        group_ids: list[str] | None = None,

        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)


        return self._put(
            "/iam/v1/urgp/user/role/group",
            body={
                "userId": user_id,
                "roleIds": role_ids,
                "groupIds": group_ids or [],
            },
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )
    def create_role_with_policies(
        self,
        *,
        role_name: str,
        description: str,
        policy_ids: list[str],

        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)


        return self._post(
            "/iam/v1/role/rolepolicies",
            body={
                "Role": {
                    "Name": role_name,
                    "Description": description,
                },
                "PolicyIDs": policy_ids,
            },
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )
    
    def get_user(
        self,
        user_krn: str,
        *,
        x_region: str | None = None,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        headers = self._auth_headers(extra_headers)
        headers.update({
            "Content-Type": "application/json",
        })
        region = (
            x_region
            or getattr(self._client, "region", None)
            or os.environ.get("KRUTRIM_REGION")
            or os.environ.get("REGION")
        )
        if region and "x-region" not in headers:
            headers["x-region"] = region

        return self._get(
            f"/iam/v1/users/{user_krn}",
            options=make_request_options(extra_headers=headers, timeout=timeout),
            cast_to=object,
        )

    def delete_user(
        self,
        user_krn: str,
        *,
        x_region: str | None = None,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        headers = self._auth_headers(extra_headers)
        headers.update({
            "Content-Type": "application/json",
        })
        region = (
            x_region
            or getattr(self._client, "region", None)
            or os.environ.get("KRUTRIM_REGION")
            or os.environ.get("REGION")
        )
        if region and "x-region" not in headers:
            headers["x-region"] = region

        return self._delete(
            f"/iam/v1/users/{user_krn}",
            options=make_request_options(extra_headers=headers, timeout=timeout),
            cast_to=object,
        )

    # -------------------------
    # LIST USERS
    # -------------------------
    def list_users(
        self,
        *,
        limit: int = 10,
        offset: int = 0,
        x_region: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        headers = self._auth_headers(extra_headers)
        region = (
            x_region
            or getattr(self._client, "region", None)
            or os.environ.get("KRUTRIM_REGION")
            or os.environ.get("REGION")
        )
        if region and "x-region" not in headers:
            headers["x-region"] = region

        query: dict[str, object] = {
            "limit": limit,
            "offset": offset,
        }
        if extra_query:
            query.update(extra_query)

        return self._get(
            "/iam/v1/users",
            options=make_request_options(
                extra_headers=headers,
                query=query,
                timeout=timeout,
            ),
            cast_to=object,
        )
# =========================
# ASYNC RESOURCE
# =========================
class AsyncIAMResource(AsyncAPIResource):

    @cached_property
    def with_raw_response(self) -> "AsyncIAMResourceWithRawResponse":
        return AsyncIAMResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> "AsyncIAMResourceWithStreamingResponse":
        return AsyncIAMResourceWithStreamingResponse(self)

    def _auth_headers(self, extra_headers: Headers | None = None) -> Headers:
        headers = {"Accept": "*/*", **(extra_headers or {})}

        token = getattr(self._client, "token", None) or getattr(self._client, "api_key", None)
        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    async def create_user(
        self,
        *,
        user_name: str,
        email: str,
        password: str,
        console_access: bool,

        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:

        headers = {"Accept": "*/*", **(extra_headers or {})}


        return await self._post(
            "/iam/v1/user",
            body={
                "user": {
                    "userName": user_name,
                    "email": email,
                    "password": password,
                    "consoleAccess": console_access,
                }
            },
            options=make_request_options(
                extra_headers=headers,
                timeout=timeout,
            ),
            cast_to=object,
        )

    async def enable_programmatic_access(
        self,
        user_krn: str,
        *,

        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)


        return await self._post(
            f"/iam/v1/users/programmaticAccess/{user_krn}",
            body={},
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )

    async def list_roles(
        self,
        *,

        limit: int = 9999,
        offset: int = 0,
        krutrim_managed: bool | str | None = None,
        krutrimManaged: bool | str | None = None,
        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)

        managed = krutrimManaged if krutrimManaged is not None else krutrim_managed
        if managed is None:
            managed_value = "all"
        elif isinstance(managed, bool):
            managed_value = "true" if managed else "false"
        else:
            managed_value = str(managed).lower()


        return await self._get(
            "/iam/v1/roles",
            options=make_request_options(
                extra_headers=headers,
                query={
                    "limit": limit,
                    "offset": offset,
                    "krutrimManaged": managed_value,
                },
            ),
            cast_to=object,
        )

    async def signin_programmatic_user(
        self,
        *,
        account_id: str,
        access_key: str,
        secret_key: str,
        extra_headers: Headers | None = None,
    ) -> object:

        headers = {"Content-Type": "application/json", **(extra_headers or {})}

        resp = await self._post(
            "/iam/v1/signinProgrammaticUser",
            body={
                "accountId": account_id,
                "accessKey": access_key,
                "secretKey": secret_key,
            },
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )

        if isinstance(resp, dict):
            token = resp.get("token") or resp.get("access_token")
            if token:
                self._client.api_key = token
                setattr(self._client, "token", token)

        return resp

    # -------------------------
    # SIGN IN AS ROOT USER
    # -------------------------
    async def sign_in_as_root_user(
        self,
        *,
        email: str,
        password: str,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        headers = {"Content-Type": "application/json", **(extra_headers or {})}

        resp = await self._post(
            "/iam/v1/signInAsRootUser",
            body={
                "email": email,
                "password": password,
            },
            options=make_request_options(
                extra_headers=headers,
                timeout=timeout,
            ),
            cast_to=object,
        )

        if isinstance(resp, dict):
            token = resp.get("access_token") or resp.get("token")
            if token:
                self._client.api_key = token
                setattr(self._client, "token", token)

        return resp

    async def get_role(
        self,
        role_krn: str,
        *,
        extra_headers: Headers | None = None,
    ) -> object:
        if not role_krn:
            raise ValueError("Expected non-empty role_krn")

        headers = self._auth_headers(extra_headers)

        return await self._get(
            f"/iam/v1/roles/{role_krn}",
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )

    async def delete_role(
        self,
        role_krn: str,
        *,
        extra_headers: Headers | None = None,
    ) -> object:
        headers = self._auth_headers(extra_headers)

        return await self._delete(
            f"/iam/v1/roles/{role_krn}",
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )

    async def attach_policies_to_role(
        self,
        *,
        role_id: str,
        policy_ids: list[str],
        extra_headers: Headers | None = None,
    ) -> object:
        headers = self._auth_headers(extra_headers)

        return await self._put(
            "/iam/v1/urgp/role/policy",
            body={
                "roleId": role_id,
                "policyIds": policy_ids,
            },
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )

    async def reset_programmatic_access(
        self,
        user_krn: str,
        *,
        extra_headers: Headers | None = None,
    ) -> object:
        headers = self._auth_headers(extra_headers)

        return await self._post(
            f"/iam/v1/users/resetProgrammaticAccess/{user_krn}",
            body={},
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )

    async def disable_programmatic_access(
        self,
        user_krn: str,
        *,
        extra_headers: Headers | None = None,
    ) -> object:
        headers = self._auth_headers(extra_headers)

        return await self._put(
            f"/iam/v1/users/disableProgrammaticAccess/{user_krn}",
            body={},
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )

    async def list_policies(
        self,
        *,
        limit: int = 10,
        offset: int = 0,
        krutrim_managed: str = "all",
        extra_headers: Headers | None = None,
    ) -> object:
        headers = self._auth_headers(extra_headers)

        return await self._get(
            "/iam/v1/policies",
            options=make_request_options(
                extra_headers=headers,
                query={
                    "limit": limit,
                    "offset": offset,
                    "krutrimManaged": str(krutrim_managed).lower(),
                },
            ),
            cast_to=object,
        )

    async def assign_roles_to_user(
        self,
        *,
        user_id: str,
        role_ids: list[str],
        group_ids: list[str] | None = None,
        extra_headers: Headers | None = None,
    ) -> object:
        headers = self._auth_headers(extra_headers)

        return await self._put(
            "/iam/v1/urgp/user/role/group",
            body={
                "userId": user_id,
                "roleIds": role_ids,
                "groupIds": group_ids or [],
            },
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )

    async def create_role_with_policies(
        self,
        *,
        role_name: str,
        description: str,
        policy_ids: list[str],
        extra_headers: Headers | None = None,
    ) -> object:
        headers = self._auth_headers(extra_headers)

        return await self._post(
            "/iam/v1/role/rolepolicies",
            body={
                "Role": {
                    "Name": role_name,
                    "Description": description,
                },
                "PolicyIDs": policy_ids,
            },
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )

    async def get_user(
        self,
        user_krn: str,
        *,
        x_region: str | None = None,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        headers = self._auth_headers(extra_headers)
        headers.update({
            "Content-Type": "application/json",
        })
        region = (
            x_region
            or getattr(self._client, "region", None)
            or os.environ.get("KRUTRIM_REGION")
            or os.environ.get("REGION")
        )
        if region and "x-region" not in headers:
            headers["x-region"] = region

        return await self._get(
            f"/iam/v1/users/{user_krn}",
            options=make_request_options(extra_headers=headers, timeout=timeout),
            cast_to=object,
        )

    async def delete_user(
        self,
        user_krn: str,
        *,
        x_region: str | None = None,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        headers = self._auth_headers(extra_headers)
        headers.update({
            "Content-Type": "application/json",
        })
        region = (
            x_region
            or getattr(self._client, "region", None)
            or os.environ.get("KRUTRIM_REGION")
            or os.environ.get("REGION")
        )
        if region and "x-region" not in headers:
            headers["x-region"] = region

        return await self._delete(
            f"/iam/v1/users/{user_krn}",
            options=make_request_options(extra_headers=headers, timeout=timeout),
            cast_to=object,
        )

    async def list_users(
        self,
        *,
        limit: int = 10,
        offset: int = 0,
        x_region: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        headers = self._auth_headers(extra_headers)
        region = (
            x_region
            or getattr(self._client, "region", None)
            or os.environ.get("KRUTRIM_REGION")
            or os.environ.get("REGION")
        )
        if region and "x-region" not in headers:
            headers["x-region"] = region

        query: dict[str, object] = {
            "limit": limit,
            "offset": offset,
        }
        if extra_query:
            query.update(extra_query)

        return await self._get(
            "/iam/v1/users",
            options=make_request_options(
                extra_headers=headers,
                query=query,
                timeout=timeout,
            ),
            cast_to=object,
        )


class IAMResourceWithRawResponse:
    def __init__(self, iam: IAMResource) -> None:
        self.create_user = to_raw_response_wrapper(iam.create_user)
        self.enable_programmatic_access = to_raw_response_wrapper(iam.enable_programmatic_access)
        self.list_roles = to_raw_response_wrapper(iam.list_roles)
        self.signin_programmatic_user = to_raw_response_wrapper(iam.signin_programmatic_user)
        self.sign_in_as_root_user = to_raw_response_wrapper(iam.sign_in_as_root_user)
        self.get_role = to_raw_response_wrapper(iam.get_role)
        self.delete_role = to_raw_response_wrapper(iam.delete_role)
        self.attach_policies_to_role = to_raw_response_wrapper(iam.attach_policies_to_role)
        self.reset_programmatic_access = to_raw_response_wrapper(iam.reset_programmatic_access)
        self.disable_programmatic_access = to_raw_response_wrapper(iam.disable_programmatic_access)
        self.list_policies = to_raw_response_wrapper(iam.list_policies)
        self.assign_roles_to_user = to_raw_response_wrapper(iam.assign_roles_to_user)
        self.create_role_with_policies = to_raw_response_wrapper(iam.create_role_with_policies)
        self.get_user = to_raw_response_wrapper(iam.get_user)
        self.delete_user = to_raw_response_wrapper(iam.delete_user)
        self.list_users = to_raw_response_wrapper(iam.list_users)


class AsyncIAMResourceWithRawResponse:
    def __init__(self, iam: AsyncIAMResource) -> None:
        self.create_user = async_to_raw_response_wrapper(iam.create_user)
        self.enable_programmatic_access = async_to_raw_response_wrapper(iam.enable_programmatic_access)
        self.list_roles = async_to_raw_response_wrapper(iam.list_roles)
        self.signin_programmatic_user = async_to_raw_response_wrapper(iam.signin_programmatic_user)
        self.sign_in_as_root_user = async_to_raw_response_wrapper(iam.sign_in_as_root_user)
        self.get_role = async_to_raw_response_wrapper(iam.get_role)
        self.delete_role = async_to_raw_response_wrapper(iam.delete_role)
        self.attach_policies_to_role = async_to_raw_response_wrapper(iam.attach_policies_to_role)
        self.reset_programmatic_access = async_to_raw_response_wrapper(iam.reset_programmatic_access)
        self.disable_programmatic_access = async_to_raw_response_wrapper(iam.disable_programmatic_access)
        self.list_policies = async_to_raw_response_wrapper(iam.list_policies)
        self.assign_roles_to_user = async_to_raw_response_wrapper(iam.assign_roles_to_user)
        self.create_role_with_policies = async_to_raw_response_wrapper(iam.create_role_with_policies)
        self.get_user = async_to_raw_response_wrapper(iam.get_user)
        self.delete_user = async_to_raw_response_wrapper(iam.delete_user)
        self.list_users = async_to_raw_response_wrapper(iam.list_users)


class IAMResourceWithStreamingResponse:
    def __init__(self, iam: IAMResource) -> None:
        self.create_user = to_streamed_response_wrapper(iam.create_user)
        self.enable_programmatic_access = to_streamed_response_wrapper(iam.enable_programmatic_access)
        self.list_roles = to_streamed_response_wrapper(iam.list_roles)
        self.signin_programmatic_user = to_streamed_response_wrapper(iam.signin_programmatic_user)
        self.sign_in_as_root_user = to_streamed_response_wrapper(iam.sign_in_as_root_user)
        self.get_role = to_streamed_response_wrapper(iam.get_role)
        self.delete_role = to_streamed_response_wrapper(iam.delete_role)
        self.attach_policies_to_role = to_streamed_response_wrapper(iam.attach_policies_to_role)
        self.reset_programmatic_access = to_streamed_response_wrapper(iam.reset_programmatic_access)
        self.disable_programmatic_access = to_streamed_response_wrapper(iam.disable_programmatic_access)
        self.list_policies = to_streamed_response_wrapper(iam.list_policies)
        self.assign_roles_to_user = to_streamed_response_wrapper(iam.assign_roles_to_user)
        self.create_role_with_policies = to_streamed_response_wrapper(iam.create_role_with_policies)
        self.get_user = to_streamed_response_wrapper(iam.get_user)
        self.delete_user = to_streamed_response_wrapper(iam.delete_user)
        self.list_users = to_streamed_response_wrapper(iam.list_users)


class AsyncIAMResourceWithStreamingResponse:
    def __init__(self, iam: AsyncIAMResource) -> None:
        self.create_user = async_to_streamed_response_wrapper(iam.create_user)
        self.enable_programmatic_access = async_to_streamed_response_wrapper(iam.enable_programmatic_access)
        self.list_roles = async_to_streamed_response_wrapper(iam.list_roles)
        self.signin_programmatic_user = async_to_streamed_response_wrapper(iam.signin_programmatic_user)
        self.sign_in_as_root_user = async_to_streamed_response_wrapper(iam.sign_in_as_root_user)
        self.get_role = async_to_streamed_response_wrapper(iam.get_role)
        self.delete_role = async_to_streamed_response_wrapper(iam.delete_role)
        self.attach_policies_to_role = async_to_streamed_response_wrapper(iam.attach_policies_to_role)
        self.reset_programmatic_access = async_to_streamed_response_wrapper(iam.reset_programmatic_access)
        self.disable_programmatic_access = async_to_streamed_response_wrapper(iam.disable_programmatic_access)
        self.list_policies = async_to_streamed_response_wrapper(iam.list_policies)
        self.assign_roles_to_user = async_to_streamed_response_wrapper(iam.assign_roles_to_user)
        self.create_role_with_policies = async_to_streamed_response_wrapper(iam.create_role_with_policies)
        self.get_user = async_to_streamed_response_wrapper(iam.get_user)
        self.delete_user = async_to_streamed_response_wrapper(iam.delete_user)
        self.list_users = async_to_streamed_response_wrapper(iam.list_users)
