from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Headers, NoneType, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options


__all__ = ["IAMResource", "AsyncIAMResource"]


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

        token = getattr(self._client, "token", None)
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
        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)


        return self._get(
            "/iam/v1/roles",
            options=make_request_options(
                extra_headers=headers,
                query={
                    "limit": limit,
                    "offset": offset,
                    "krutrimManaged": "all",
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
                setattr(self._client, "token", token)

        return resp

    def get_role(
        self,
        role_krn: str,
        *,

        extra_headers: Headers | None = None,
    ) -> object:

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
        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)
        headers.update({
            "Content-Type": "application/json",
  
        })

        return self._get(
            f"/iam/v1/users/{user_krn}",
            options=make_request_options(extra_headers=headers),
            cast_to=object,
        )
    def delete_user(
        self,
        user_krn: str,
        *,

        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)
        headers.update({
            "Content-Type": "application/json",

        })

        return self._delete(
            f"/iam/v1/users/{user_krn}",
            options=make_request_options(extra_headers=headers),
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

        token = getattr(self._client, "token", None)
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
        extra_headers: Headers | None = None,
    ) -> object:

        headers = self._auth_headers(extra_headers)


        return await self._get(
            "/iam/v1/roles",
            options=make_request_options(
                extra_headers=headers,
                query={
                    "limit": limit,
                    "offset": offset,
                    "krutrimManaged": "all",
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
                setattr(self._client, "token", token)

        return resp



class IAMResourceWithRawResponse:
    def __init__(self, iam: IAMResource) -> None:
        self.create_user = to_raw_response_wrapper(iam.create_user)
        self.enable_programmatic_access = to_raw_response_wrapper(iam.enable_programmatic_access)
        self.list_roles = to_raw_response_wrapper(iam.list_roles)
        self.signin_programmatic_user = to_raw_response_wrapper(iam.signin_programmatic_user)


class AsyncIAMResourceWithRawResponse:
    def __init__(self, iam: AsyncIAMResource) -> None:
        self.create_user = async_to_raw_response_wrapper(iam.create_user)
        self.enable_programmatic_access = async_to_raw_response_wrapper(iam.enable_programmatic_access)
        self.list_roles = async_to_raw_response_wrapper(iam.list_roles)
        self.signin_programmatic_user = async_to_raw_response_wrapper(iam.signin_programmatic_user)


class IAMResourceWithStreamingResponse:
    def __init__(self, iam: IAMResource) -> None:
        self.create_user = to_streamed_response_wrapper(iam.create_user)
        self.enable_programmatic_access = to_streamed_response_wrapper(iam.enable_programmatic_access)
        self.list_roles = to_streamed_response_wrapper(iam.list_roles)
        self.signin_programmatic_user = to_streamed_response_wrapper(iam.signin_programmatic_user)


class AsyncIAMResourceWithStreamingResponse:
    def __init__(self, iam: AsyncIAMResource) -> None:
        self.create_user = async_to_streamed_response_wrapper(iam.create_user)
        self.enable_programmatic_access = async_to_streamed_response_wrapper(iam.enable_programmatic_access)
        self.list_roles = async_to_streamed_response_wrapper(iam.list_roles)
        self.signin_programmatic_user = async_to_streamed_response_wrapper(iam.signin_programmatic_user)