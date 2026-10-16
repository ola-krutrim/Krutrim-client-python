from __future__ import annotations

import os
from typing import Any, Union, Mapping
from pathlib import Path
from typing_extensions import Self, Literal, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import kbs, sshkey, highlvlvpc, startStopVM, securityGroup
from ._constants import CLOUD_BASE_URL, CLOUDX_BASE_URL
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.lb import lb
from .resources.v1 import v1, record
from .resources.asg import asg, asgV1
from .resources.iam import iam
from .resources.kcm import tags, certs
from .resources.kks import kks
from .resources.kos import kos
from .resources.kpod import kpod
from .resources.sandbox import (
    SandboxResource,
    AsyncSandboxResource,
    SandboxResourceWithRawResponse,
    AsyncSandboxResourceWithRawResponse,
    SandboxResourceWithStreamingResponse,
    AsyncSandboxResourceWithStreamingResponse,
)
from .resources.v1.zone import vpc, zone
from .resources.kks.clusters import addons, clusters, node_groups

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "KrutrimClient",
    "AsyncKrutrimClient",
    "Client",
    "AsyncClient",
    "Environment",
    "ENVIRONMENTS",
]


_DOTENV_LOADED = False


def _load_dotenv_if_present() -> None:
    global _DOTENV_LOADED
    if _DOTENV_LOADED:
        return
    _DOTENV_LOADED = True

    try:
        from dotenv import load_dotenv  # type: ignore[import-untyped]

        load_dotenv()
        return
    except ImportError:
        pass

    try:
        cwd = Path.cwd()
        for directory in [cwd, *cwd.parents]:
            env_file = directory / ".env"
            if env_file.is_file():
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v
                break
    except Exception:
        pass


Environment = Literal["production", "cloud", "cloudx"]

ENVIRONMENTS: dict[str, str] = {
    "cloud": CLOUD_BASE_URL,
    "cloudx": CLOUDX_BASE_URL,
    "production": CLOUD_BASE_URL,
    "prod": CLOUD_BASE_URL,
    "stage": CLOUDX_BASE_URL,
    "staging": CLOUDX_BASE_URL,
    "cloud.olakrutrim.com": CLOUD_BASE_URL,
    "https://cloud.olakrutrim.com": CLOUD_BASE_URL,
    "cloudx.olakrutrim.com": CLOUDX_BASE_URL,
    "https://cloudx.olakrutrim.com": CLOUDX_BASE_URL,
}

_DEFAULT_ENVIRONMENT: Environment = "cloud"
_DEFAULT_BASE_URL: str = CLOUD_BASE_URL


def _resolve_base_url(
    *,
    base_url: str | httpx.URL | None = None,
    environment: Environment | str | None = None,
) -> str | httpx.URL:
    if base_url is not None and environment is not None:
        raise ValueError("Both base_url and environment were given; only one should be sent")

    if base_url is not None:
        return base_url

    if environment is not None:
        norm_env = environment.strip().lower().rstrip("/") if isinstance(environment, str) else environment
        if norm_env in ENVIRONMENTS:
            return ENVIRONMENTS[norm_env]
        raise ValueError(f"Unknown environment: {environment!r}. Must be one of: {list(ENVIRONMENTS.keys())}")

    for env_var in (
        "KRUTRIMCLIENT_BASE_URL",
        "krutrim_client_BASE_URL",
        "KRUTRIM_CLIENT_BASE_URL",
        "KRUTRIM_BASE_URL",
        "BASE_URL",
    ):
        url = os.environ.get(env_var)
        if url:
            return url

    env_name = (
        os.environ.get("KRUTRIM_ENVIRONMENT")
        or os.environ.get("KRUTRIMCLIENT_ENVIRONMENT")
        or os.environ.get("KRUTRIM_CLIENT_ENVIRONMENT")
        or os.environ.get("ENVIRONMENT")
        or os.environ.get("ENV")
    )
    if env_name:
        norm_env = env_name.strip().lower().rstrip("/")
        if norm_env in ENVIRONMENTS:
            return ENVIRONMENTS[norm_env]
        raise ValueError(f"Unknown environment from env var: {env_name!r}. Must be one of: {list(ENVIRONMENTS.keys())}")

    return _DEFAULT_BASE_URL


class KrutrimClient(SyncAPIClient):
    sandbox: SandboxResource
    highlvlvpc: highlvlvpc.HighlvlvpcResource
    kbs: kbs.KbsResource
    securityGroup: securityGroup.SecurityGroupResource
    startStopVM: startStopVM.StartStopResource
    sshkey :sshkey.SshkeysResource
    kpod: kpod.KpodResource
    kos: kos.KosResource
    lb: lb.HighlvlResource
    kks: kks.KksResource
    v1: v1.V1Resource
    addons: addons.AddonsResource
    clusters: clusters.ClustersResource
    node_groups: node_groups.NodeGroupsResource  
    record: record.RecordResource
    vpc: vpc.VpcResource
    zone: zone.ZoneResource  
    certs: certs.CertsResource
    tags: tags.TagsResource
    asg: asg.AsgResource
    asgV1: asgV1.V1Resource
    iam: iam.IAMResource

    
    with_raw_response: KrutrimClientWithRawResponse
    with_streaming_response: KrutrimClientWithStreamedResponse

    # client options
    api_key: str
    region: str | None = None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        environment: Environment | None = None,
        region: str | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous KrutrimClient client instance.

        This automatically infers the `api_key` argument from the `KRUTRIMCLIENT_API_KEY` environment variable if it is not provided.
        Set `environment` to `"cloud"` or `"cloudx"` to select the matching
        Krutrim endpoint. Pass either `environment` or `base_url`, not both.
        """
        _load_dotenv_if_present()
        if api_key is None:
            api_key = (
                os.environ.get("KRUTRIMCLIENT_API_KEY")
                or os.environ.get("KRUTRIM_API_KEY")
                or os.environ.get("API_KEY")
            )
        if api_key is None:
            api_key = ""
        self.api_key = api_key

        if region is None:
            region = os.environ.get("KRUTRIM_REGION") or os.environ.get("REGION")
        self.region = region

        base_url = _resolve_base_url(base_url=base_url, environment=environment)

        resolved_headers = dict(default_headers) if default_headers else {}
        if self.region and "x-region" not in httpx.Headers(resolved_headers):
            resolved_headers["x-region"] = self.region

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=resolved_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.highlvlvpc = highlvlvpc.HighlvlvpcResource(self)
        self.kbs =  kbs.KbsResource(self)
        self.securityGroup = securityGroup.SecurityGroupResource(self)
        self.startStopVM = startStopVM.StartStopResource(self)
        self.sshkey = sshkey.SshkeysResource(self)
        self.kpod = kpod.KpodResource(self)
        self.kos = kos.KosResource(self)
        self.lb = lb.HighlvlResource(self)
        self.certs = certs.CertsResource(self)
        self.tags = tags.TagsResource(self)
        self.asg = asg.AsgResource(self)
        self.asgV1 = asgV1.V1Resource(self)
        self.kks = kks.KksResource(self)
        self.v1 = v1.V1Resource(self)
        self.addons = addons.AddonsResource(self)    
        self.clusters = clusters.ClustersResource(self)
        self.node_groups = node_groups.NodeGroupsResource(self)
        self.record = record.RecordResource(self)
        self.zone = zone.ZoneResource(self)
        self.vpc = vpc.VpcResource(self)
        self.iam = iam.IAMResource(self)
        self.sandbox = SandboxResource(self)
        self.with_raw_response = KrutrimClientWithRawResponse(self)
        self.with_streaming_response = KrutrimClientWithStreamedResponse(self)

        

        

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        token = getattr(self, "token", None) or self.api_key
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        environment: Environment | None = None,
        region: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = dict(self._custom_headers)
        if region is not None and self.region is not None:
            headers = {
                key: value
                for key, value in headers.items()
                if key.lower() != "x-region" or value != self.region
            }
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        if base_url is not None or environment is not None:
            resolved_base_url = _resolve_base_url(base_url=base_url, environment=environment)
        else:
            resolved_base_url = self.base_url

        http_client = http_client or self._client
        return self.__class__(
            api_key=self.api_key if api_key is None else api_key,
            base_url=resolved_base_url,
            region=self.region if region is None else region,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncKrutrimClient(AsyncAPIClient):
    sandbox: AsyncSandboxResource
    highlvlvpc: highlvlvpc.AsyncHighlvlvpcResource
    kbs: kbs.AsyncKbsResource
    securityGroup: securityGroup.AsyncSecurityGroupResource
    startStopVM: startStopVM.AsyncStartStopResource
    sshkey: sshkey.AsyncSshkeysResource
    kpod: kpod.AsyncKpodResource
    kos: kos.AsyncKosResource 
    lb: lb.AsyncHighlvlResource
    certs: certs.AsyncCertsResource
    tags: tags.AsyncTagsResource
    asg: asg.AsyncAsgResource
    asgV1: asgV1.AsyncV1Resource
    Kks: kks.AsyncKksResource
    v1: v1.AsyncV1Resource
    clusters: clusters.AsyncClustersResource
    node_groups: node_groups.AsyncNodeGroupsResource
    addons: addons.AsyncAddonsResource
    record: record.AsyncRecordResource
    zone: zone.AsyncZoneResource
    vpc: vpc.AsyncVpcResource
    iam: iam.AsyncIAMResource 
    
    with_raw_response: AsyncKrutrimClientWithRawResponse
    with_streaming_response: AsyncKrutrimClientWithStreamedResponse

    # client options
    api_key: str
    region: str | None = None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        environment: Environment | None = None,
        region: str | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncKrutrimClient client instance.

        This automatically infers the `api_key` argument from the `KRUTRIMCLIENT_API_KEY` environment variable if it is not provided.
        Set `environment` to `"cloud"` or `"cloudx"` to select the matching
        Krutrim endpoint. Pass either `environment` or `base_url`, not both.
        """
        _load_dotenv_if_present()
        if api_key is None:
            api_key = (
                os.environ.get("KRUTRIMCLIENT_API_KEY")
                or os.environ.get("KRUTRIM_API_KEY")
                or os.environ.get("API_KEY")
            )
        if api_key is None:
            api_key = ""
        self.api_key = api_key

        if region is None:
            region = os.environ.get("KRUTRIM_REGION") or os.environ.get("REGION")
        self.region = region

        base_url = _resolve_base_url(base_url=base_url, environment=environment)

        resolved_headers = dict(default_headers) if default_headers else {}
        if self.region and "x-region" not in httpx.Headers(resolved_headers):
            resolved_headers["x-region"] = self.region

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=resolved_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.highlvlvpc = highlvlvpc.AsyncHighlvlvpcResource(self)
        self.kbs = kbs.AsyncKbsResource(self)
        self.securityGroup = securityGroup.AsyncSecurityGroupResource(self)
        self.startStopVM = startStopVM.AsyncStartStopResource(self)
        self.sshkey = sshkey.AsyncSshkeysResource(self)
        self.kpod = kpod.AsyncKpodResource(self)
        self.kos = kos.AsyncKosResource(self)
        self.lb = lb.AsyncHighlvlResource(self)
        self.certs = certs.AsyncCertsResource(self)
        self.tags = tags.AsyncTagsResource(self)
        self.asg = asg.AsyncAsgResource(self)
        self.asgV1 = asgV1.AsyncV1Resource(self)
        self.kks = kks.AsyncKksResource(self)
        self.v1 = v1.AsyncV1Resource(self)
        self.addons = addons.AsyncAddonsResource(self)
        self.clusters = clusters.AsyncClustersResource(self)
        self.node_groups = node_groups.AsyncNodeGroupsResource(self)
        self.record = record.AsyncRecordResource(self)
        self.vpc = vpc.AsyncVpcResource(self)
        self.zone = zone.AsyncZoneResource(self)
        self.iam = iam.AsyncIAMResource(self)
        self.sandbox = AsyncSandboxResource(self)
        self.with_raw_response = AsyncKrutrimClientWithRawResponse(self)
        self.with_streaming_response = AsyncKrutrimClientWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        token = getattr(self, "token", None) or self.api_key
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        environment: Environment | None = None,
        region: str | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = dict(self._custom_headers)
        if region is not None and self.region is not None:
            headers = {
                key: value
                for key, value in headers.items()
                if key.lower() != "x-region" or value != self.region
            }
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        if base_url is not None or environment is not None:
            resolved_base_url = _resolve_base_url(base_url=base_url, environment=environment)
        else:
            resolved_base_url = self.base_url

        http_client = http_client or self._client
        return self.__class__(
            api_key=self.api_key if api_key is None else api_key,
            base_url=resolved_base_url,
            region=self.region if region is None else region,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class KrutrimClientWithRawResponse:
    def __init__(self, client: KrutrimClient) -> None:
        self.sandbox = SandboxResourceWithRawResponse(client.sandbox)
        self.highlvlvpc = highlvlvpc.HighlvlvpcResourceWithRawResponse(client.highlvlvpc)
        self.kbs = kbs.KbsResourceWithRawResponse(client.kbs)
        self.securityGroup = securityGroup.SecurityGroupResourceWithRawResponse(client.securityGroup)
        self.startStopVM = startStopVM.StartStopResourceWithRawResponse(client.startStopVM)
        self.sshkey = sshkey.SshkeysResourceWithRawResponse(client.sshkey)
        self.kpod = kpod.KpodResourceWithRawResponse(client.kpod)
        self.kos =kos.KosResourceWithRawResponse(client.kos)
        self.lb = lb.HighlvlResourceWithRawResponse(client.lb)
        self.certs = certs.CertsResourceWithRawResponse(client.certs)
        self.tags = tags.TagsResourceWithRawResponse(client.tags)
        self.asg = asg.AsgResourceWithRawResponse(client.asg)
        self.asgV1 = asgV1.V1ResourceWithRawResponse(client.asgV1)

        self.kks = kks.KksResourceWithRawResponse(client.kks)
        self.v1 = v1.V1ResourceWithRawResponse(client.v1)
        self.addons = addons.AddonsResourceWithRawResponse(client.addons)
        self.clusters = clusters.ClustersResourceWithRawResponse(client.clusters)
        self.node_groups = node_groups.NodeGroupsResourceWithRawResponse(client.node_groups)   
        self.record = record.RecordResourceWithRawResponse(client.record)
        self.zone = zone.ZoneResourceWithRawResponse(client.zone)   
        self.vpc = vpc.VpcResourceWithRawResponse(client.vpc)

class AsyncKrutrimClientWithRawResponse:
    def __init__(self, client: AsyncKrutrimClient) -> None:
        self.sandbox = AsyncSandboxResourceWithRawResponse(client.sandbox)
        self.highlvlvpc = highlvlvpc.AsyncHighlvlvpcResourceWithRawResponse(client.highlvlvpc)
        self.kbs = kbs.AsyncKbsResourceWithRawResponse(client.kbs)
        self.securityGroup = securityGroup.AsyncSecurityGroupResourceWithRawResponse(client.securityGroup)
        self.startStopVM = startStopVM.AsyncStartStopResourceWithRawResponse(client.startStopVM)
        self.sshkey = sshkey.AsyncSshkeysResourceWithRawResponse(client.sshkey)
        self.kpod = kpod.AsyncKpodResourceWithRawResponse(client.kpod)
        self.kos = kos.AsyncKosResourceWithRawResponse(client.kos)
        self.lb = lb.AsyncHighlvlResourceWithRawResponse(client.lb)
        self.certs = certs.AsyncCertsResourceWithRawResponse(client.certs)
        self.tags = tags.AsyncTagsResourceWithRawResponse(client.tags)
        self.asg = asg.AsyncAsgResourceWithRawResponse(client.asg)
        self.asgV1 = asgV1.AsyncV1ResourceWithRawResponse(client.asgV1)
        self.kks = kks.AsyncKksResourceWithRawResponse(client.kks)
        self.v1 = v1.AsyncV1ResourceWithRawResponse(client.v1)
        self.addons = addons.AsyncAddonsResourceWithRawResponse(client.addons)    
        self.clusters = clusters.AsyncClustersResourceWithRawResponse(client.clusters)
        self.node_groups = node_groups.AsyncNodeGroupsResourceWithRawResponse(client.node_groups)
        self.record = record.AsyncRecordResourceWithRawResponse(client.record)
        self.zone = zone.AsyncZoneResourceWithRawResponse(client.zone)
        self.vpc = vpc.AsyncVpcResourceWithRawResponse(client.vpc)


class KrutrimClientWithStreamedResponse:
    def __init__(self, client: KrutrimClient) -> None:
        self.sandbox = SandboxResourceWithStreamingResponse(client.sandbox)
        self.highlvlvpc = highlvlvpc.HighlvlvpcResourceWithStreamingResponse(client.highlvlvpc)
        self.kbs = kbs.KbsResourceWithStreamingResponse(client.kbs)
        self.securityGroup = securityGroup.SecurityGroupResourceWithStreamingResponse(client.securityGroup)
        self.startStopVM = startStopVM.StartStopResourceWithStreamingResponse(client.startStopVM)
        self.sshkey = sshkey.SshkeysResourceWithStreamingResponse(client.sshkey)
        self.kpod = kpod.KpodResourceWithStreamingResponse(client.kpod)
        self.kos = kos.KosResourceWithStreamingResponse(client.kos)
        self.lb = lb.HighlvlResourceWithStreamingResponse(client.lb)
        self.certs = certs.CertsResourceWithStreamingResponse(client.certs)
        self.tags = tags.TagsResourceWithStreamingResponse(client.tags)
        self.asg = asg.AsgResourceWithStreamingResponse(client.asg)
        self.asgV1 = asgV1.V1ResourceWithStreamingResponse(client.asgV1)
        self.kks = kks.KksResourceWithStreamingResponse(client.kks)
        self.v1 = v1.V1ResourceWithStreamingResponse(client.v1)
        self.addons = addons.AddonsResourceWithStreamingResponse(client.addons)
        self.clusters = clusters.ClustersResourceWithStreamingResponse(client.clusters)
        self.node_groups = node_groups.NodeGroupsResourceWithStreamingResponse(client.node_groups)
        self.record = record.RecordResourceWithStreamingResponse(client.record)
        self.zone = zone.ZoneResourceWithStreamingResponse(client.zone)
        self.vpc = vpc.VpcResourceWithStreamingResponse(client.vpc)
        
        

class AsyncKrutrimClientWithStreamedResponse:
    def __init__(self, client: AsyncKrutrimClient) -> None:
        self.sandbox = AsyncSandboxResourceWithStreamingResponse(client.sandbox)
        self.highlvlvpc = highlvlvpc.AsyncHighlvlvpcResourceWithStreamingResponse(client.highlvlvpc)
        self.kbs = kbs.AsyncKbsResourceWithStreamingResponse(client.kbs)
        self.securityGroup = securityGroup.AsyncSecurityGroupResourceWithStreamingResponse(client.securityGroup)
        self.startStopVM = startStopVM.AsyncStartStopResourceWithStreamingResponse(client.startStopVM)
        self.sshkey = sshkey.AsyncSshkeysResourceWithStreamingResponse(client.sshkey)
        self.kpod = kpod.AsyncKpodResourceWithStreamingResponse(client.kpod)
        self.kos = kos.AsyncKosResourceWithStreamingResponse(client.kos)
        self.lb = lb.AsyncHighlvlResourceWithStreamingResponse(client.lb)
        self.certs = certs.AsyncCertsResourceWithStreamingResponse(client.certs)
        self.tags = tags.AsyncTagsResourceWithStreamingResponse(client.tags)
        self.asg = asg.AsyncAsgResourceWithStreamingResponse(client.asg)
        self.asgV1 = asgV1.AsyncV1ResourceWithStreamingResponse(client.asgV1)
        self.kks = kks.AsyncKksResourceWithStreamingResponse(client.kks)
        self.v1 =  v1.AsyncV1ResourceWithStreamingResponse(client.v1)
        self.addons = addons.AsyncAddonsResourceWithStreamingResponse(client.addons)
        self.clusters = clusters.AsyncClustersResourceWithStreamingResponse(client.clusters)
        self.node_groups = node_groups.AsyncNodeGroupsResourceWithStreamingResponse(client.node_groups)
        self.record = record.AsyncRecordResourceWithStreamingResponse(client.record)
        self.zone = zone.AsyncZoneResourceWithStreamingResponse(client.zone)
        self.vpc = vpc.AsyncVpcResourceWithStreamingResponse(client.vpc)        

Client = KrutrimClient

AsyncClient = AsyncKrutrimClient


