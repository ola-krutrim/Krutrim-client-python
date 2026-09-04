from __future__ import annotations

import time
import uuid
from types import TracebackType
from typing import IO, Any, List, Union, Literal, Mapping, Sequence, cast
from typing_extensions import TypeAlias

import httpx

from .api import (
    SandboxAPIResource,
    AsyncSandboxAPIResource,
    SandboxAPIResourceWithRawResponse,
    AsyncSandboxAPIResourceWithRawResponse,
    SandboxAPIResourceWithStreamingResponse,
    AsyncSandboxAPIResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._exceptions import NotFoundError, SandboxException, SandboxTimeoutError
from ...types.sandbox import (
    SandboxFileData,
    SandboxPortInfo,
    SandboxResponse,
    SandboxEntryInfo,
    SandboxCommandResult,
    NetworkStorageAttachmentInput,
)

__all__ = ["SandboxResource", "AsyncSandboxResource", "Sandbox", "AsyncSandbox"]


RequestTimeout: TypeAlias = Union[float, httpx.Timeout, None, NotGiven]


def _generated_name() -> str:
    return f"sandbox-{uuid.uuid4().hex[:12]}"


def _validate_wait_timeout(wait_timeout: float) -> None:
    if wait_timeout <= 0:
        raise ValueError("wait_timeout must be greater than zero")


def _metadata_id(metadata: SandboxResponse, fallback: str | None = None) -> str:
    sandbox_id = metadata.id or fallback
    if not sandbox_id:
        raise SandboxException(
            "Sandbox response did not include an identifier", sandbox_id="unknown", metadata=metadata
        )
    return sandbox_id


def _missing_data(operation: str, sandbox_id: str, metadata: object | None = None) -> SandboxException:
    return SandboxException(
        f"Sandbox {operation} response did not include expected data",
        sandbox_id=sandbox_id,
        metadata=metadata,
    )


def _attach_cleanup_error(exc: BaseException, cleanup_error: BaseException) -> None:
    add_note = getattr(exc, "add_note", None)
    if callable(add_note):
        add_note(f"Sandbox cleanup also failed: {cleanup_error!r}")
    try:
        cast(Any, exc).__sandbox_cleanup_error__ = cleanup_error
    except Exception:
        pass


class SandboxResource(SyncAPIResource):
    @cached_property
    def api(self) -> SandboxAPIResource:
        return SandboxAPIResource(self._client)

    @cached_property
    def with_raw_response(self) -> SandboxResourceWithRawResponse:
        return SandboxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SandboxResourceWithStreamingResponse:
        return SandboxResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        flavor_name: str,
        region: str,
        sandbox_name: str | None = None,
        template_id: int | None = None,
        template_name: str | None = None,
        network_storages: Sequence[NetworkStorageAttachmentInput] | None = None,
        environment_variables: Mapping[str, str] | None = None,
        timeout: int | None = None,
        wait_timeout: float = 300.0,
        request_timeout: RequestTimeout = NOT_GIVEN,
    ) -> Sandbox:
        created = self.api.create(
            sandbox_name=sandbox_name or _generated_name(),
            region=region,
            flavor_name=flavor_name,
            template_id=template_id,
            template_name=template_name,
            network_storages=network_storages,
            environment_variables=environment_variables,
            ttl_seconds=timeout,
            timeout=request_timeout,
        )
        if created.data is None or not created.data.id:
            raise SandboxException(
                "Sandbox create response did not include an identifier",
                sandbox_id="unknown",
                metadata=created.data,
            )
        metadata = self._wait_until_active(
            created.data.id,
            wait_timeout=wait_timeout,
            request_timeout=request_timeout,
            allow_initial_not_found=True,
        )
        return Sandbox(self.api, metadata)

    def connect(
        self,
        sandbox_id: str,
        *,
        wait_timeout: float = 300.0,
        request_timeout: RequestTimeout = NOT_GIVEN,
    ) -> Sandbox:
        metadata = self._wait_until_active(
            sandbox_id,
            wait_timeout=wait_timeout,
            request_timeout=request_timeout,
        )
        return Sandbox(self.api, metadata, sandbox_id=sandbox_id)

    def _wait_until_active(
        self,
        sandbox_id: str,
        *,
        wait_timeout: float,
        request_timeout: RequestTimeout,
        allow_initial_not_found: bool = False,
    ) -> SandboxResponse:
        _validate_wait_timeout(wait_timeout)
        deadline = time.monotonic() + wait_timeout
        delay = 0.25
        last_metadata: SandboxResponse | None = None
        while True:
            try:
                response = self.api.retrieve(sandbox_id, timeout=request_timeout)
            except NotFoundError as exc:
                if allow_initial_not_found and last_metadata is None:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise SandboxTimeoutError(
                            "Timed out waiting for sandbox to become visible",
                            sandbox_id=sandbox_id,
                            metadata=None,
                        ) from exc
                    self._sleep(min(delay, remaining))
                    delay = min(delay * 2, 2.0)
                    continue
                raise SandboxException(
                    "Sandbox disappeared while waiting for readiness",
                    sandbox_id=sandbox_id,
                    metadata=last_metadata,
                ) from exc
            metadata = response.data
            if metadata is None:
                raise _missing_data("retrieve", sandbox_id, last_metadata)
            last_metadata = metadata
            if metadata.status == "active":
                return metadata
            if metadata.status == "failed_deploy":
                raise SandboxException(
                    metadata.error_message or "Sandbox deployment failed",
                    sandbox_id=sandbox_id,
                    metadata=metadata,
                )
            if metadata.status == "deleting":
                raise SandboxException(
                    "Sandbox entered deleting state while waiting for readiness",
                    sandbox_id=sandbox_id,
                    metadata=metadata,
                )
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise SandboxTimeoutError(
                    "Timed out waiting for sandbox to become active",
                    sandbox_id=sandbox_id,
                    metadata=metadata,
                )
            self._sleep(min(delay, remaining))
            delay = min(delay * 2, 2.0)


class AsyncSandboxResource(AsyncAPIResource):
    @cached_property
    def api(self) -> AsyncSandboxAPIResource:
        return AsyncSandboxAPIResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSandboxResourceWithRawResponse:
        return AsyncSandboxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSandboxResourceWithStreamingResponse:
        return AsyncSandboxResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        flavor_name: str,
        region: str,
        sandbox_name: str | None = None,
        template_id: int | None = None,
        template_name: str | None = None,
        network_storages: Sequence[NetworkStorageAttachmentInput] | None = None,
        environment_variables: Mapping[str, str] | None = None,
        timeout: int | None = None,
        wait_timeout: float = 300.0,
        request_timeout: RequestTimeout = NOT_GIVEN,
    ) -> AsyncSandbox:
        created = await self.api.create(
            sandbox_name=sandbox_name or _generated_name(),
            region=region,
            flavor_name=flavor_name,
            template_id=template_id,
            template_name=template_name,
            network_storages=network_storages,
            environment_variables=environment_variables,
            ttl_seconds=timeout,
            timeout=request_timeout,
        )
        if created.data is None or not created.data.id:
            raise SandboxException(
                "Sandbox create response did not include an identifier",
                sandbox_id="unknown",
                metadata=created.data,
            )
        metadata = await self._wait_until_active(
            created.data.id,
            wait_timeout=wait_timeout,
            request_timeout=request_timeout,
            allow_initial_not_found=True,
        )
        return AsyncSandbox(self.api, metadata)

    async def connect(
        self,
        sandbox_id: str,
        *,
        wait_timeout: float = 300.0,
        request_timeout: RequestTimeout = NOT_GIVEN,
    ) -> AsyncSandbox:
        metadata = await self._wait_until_active(
            sandbox_id,
            wait_timeout=wait_timeout,
            request_timeout=request_timeout,
        )
        return AsyncSandbox(self.api, metadata, sandbox_id=sandbox_id)

    async def _wait_until_active(
        self,
        sandbox_id: str,
        *,
        wait_timeout: float,
        request_timeout: RequestTimeout,
        allow_initial_not_found: bool = False,
    ) -> SandboxResponse:
        _validate_wait_timeout(wait_timeout)
        deadline = time.monotonic() + wait_timeout
        delay = 0.25
        last_metadata: SandboxResponse | None = None
        while True:
            try:
                response = await self.api.retrieve(sandbox_id, timeout=request_timeout)
            except NotFoundError as exc:
                if allow_initial_not_found and last_metadata is None:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise SandboxTimeoutError(
                            "Timed out waiting for sandbox to become visible",
                            sandbox_id=sandbox_id,
                            metadata=None,
                        ) from exc
                    await self._sleep(min(delay, remaining))
                    delay = min(delay * 2, 2.0)
                    continue
                raise SandboxException(
                    "Sandbox disappeared while waiting for readiness",
                    sandbox_id=sandbox_id,
                    metadata=last_metadata,
                ) from exc
            metadata = response.data
            if metadata is None:
                raise _missing_data("retrieve", sandbox_id, last_metadata)
            last_metadata = metadata
            if metadata.status == "active":
                return metadata
            if metadata.status == "failed_deploy":
                raise SandboxException(
                    metadata.error_message or "Sandbox deployment failed",
                    sandbox_id=sandbox_id,
                    metadata=metadata,
                )
            if metadata.status == "deleting":
                raise SandboxException(
                    "Sandbox entered deleting state while waiting for readiness",
                    sandbox_id=sandbox_id,
                    metadata=metadata,
                )
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise SandboxTimeoutError(
                    "Timed out waiting for sandbox to become active",
                    sandbox_id=sandbox_id,
                    metadata=metadata,
                )
            await self._sleep(min(delay, remaining))
            delay = min(delay * 2, 2.0)


class Sandbox:
    def __init__(
        self,
        api: SandboxAPIResource,
        metadata: SandboxResponse,
        *,
        sandbox_id: str | None = None,
    ) -> None:
        self._api = api
        self._metadata = metadata
        self._sandbox_id = _metadata_id(metadata, sandbox_id)
        self._killed = False

    @property
    def sandbox_id(self) -> str:
        return self._sandbox_id

    @property
    def sandbox_krn(self) -> str | None:
        return self._metadata.krn

    @property
    def metadata(self) -> SandboxResponse:
        return self._metadata

    @cached_property
    def files(self) -> SandboxFiles:
        return SandboxFiles(self)

    @cached_property
    def commands(self) -> SandboxCommands:
        return SandboxCommands(self)

    @cached_property
    def ports(self) -> SandboxPorts:
        return SandboxPorts(self)

    @cached_property
    def proxy(self) -> SandboxProxy:
        return SandboxProxy(self)

    def set_timeout(self, timeout: int, *, request_timeout: RequestTimeout = NOT_GIVEN) -> None:
        response = self._api.set_ttl(self.sandbox_id, timeout, timeout=request_timeout)
        if response.data is not None:
            self._metadata.ttl_seconds = response.data.ttl_seconds
            self._metadata.expires_at = response.data.expires_at

    def is_running(self, *, request_timeout: RequestTimeout = NOT_GIVEN) -> bool:
        try:
            response = self._api.retrieve(self.sandbox_id, timeout=request_timeout)
        except NotFoundError:
            return False
        if response.data is None:
            raise _missing_data("retrieve", self.sandbox_id, self._metadata)
        self._metadata = response.data
        return response.data.status == "active"

    def kill(self, *, request_timeout: RequestTimeout = NOT_GIVEN) -> None:
        if self._killed:
            return
        try:
            self._api.delete(self.sandbox_id, timeout=request_timeout)
        except NotFoundError:
            pass
        self._killed = True

    def run_command(
        self,
        command: str,
        *,
        cwd: str | None = None,
        envs: Mapping[str, str] | None = None,
        timeout: int = 60,
        request_timeout: RequestTimeout = NOT_GIVEN,
    ) -> SandboxCommandResult:
        return self.commands.run(
            command,
            cwd=cwd,
            envs=envs,
            timeout=timeout,
            request_timeout=request_timeout,
        )

    def __enter__(self) -> Sandbox:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        try:
            self.kill()
        except BaseException as cleanup_error:
            if exc is None:
                raise
            _attach_cleanup_error(exc, cleanup_error)
        return False


class AsyncSandbox:
    def __init__(
        self,
        api: AsyncSandboxAPIResource,
        metadata: SandboxResponse,
        *,
        sandbox_id: str | None = None,
    ) -> None:
        self._api = api
        self._metadata = metadata
        self._sandbox_id = _metadata_id(metadata, sandbox_id)
        self._killed = False

    @property
    def sandbox_id(self) -> str:
        return self._sandbox_id

    @property
    def sandbox_krn(self) -> str | None:
        return self._metadata.krn

    @property
    def metadata(self) -> SandboxResponse:
        return self._metadata

    @cached_property
    def files(self) -> AsyncSandboxFiles:
        return AsyncSandboxFiles(self)

    @cached_property
    def commands(self) -> AsyncSandboxCommands:
        return AsyncSandboxCommands(self)

    @cached_property
    def ports(self) -> AsyncSandboxPorts:
        return AsyncSandboxPorts(self)

    @cached_property
    def proxy(self) -> AsyncSandboxProxy:
        return AsyncSandboxProxy(self)

    async def set_timeout(self, timeout: int, *, request_timeout: RequestTimeout = NOT_GIVEN) -> None:
        response = await self._api.set_ttl(self.sandbox_id, timeout, timeout=request_timeout)
        if response.data is not None:
            self._metadata.ttl_seconds = response.data.ttl_seconds
            self._metadata.expires_at = response.data.expires_at

    async def is_running(self, *, request_timeout: RequestTimeout = NOT_GIVEN) -> bool:
        try:
            response = await self._api.retrieve(self.sandbox_id, timeout=request_timeout)
        except NotFoundError:
            return False
        if response.data is None:
            raise _missing_data("retrieve", self.sandbox_id, self._metadata)
        self._metadata = response.data
        return response.data.status == "active"

    async def kill(self, *, request_timeout: RequestTimeout = NOT_GIVEN) -> None:
        if self._killed:
            return
        try:
            await self._api.delete(self.sandbox_id, timeout=request_timeout)
        except NotFoundError:
            pass
        self._killed = True

    async def run_command(
        self,
        command: str,
        *,
        cwd: str | None = None,
        envs: Mapping[str, str] | None = None,
        timeout: int = 60,
        request_timeout: RequestTimeout = NOT_GIVEN,
    ) -> SandboxCommandResult:
        return await self.commands.run(
            command,
            cwd=cwd,
            envs=envs,
            timeout=timeout,
            request_timeout=request_timeout,
        )

    async def __aenter__(self) -> AsyncSandbox:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        try:
            await self.kill()
        except BaseException as cleanup_error:
            if exc is None:
                raise
            _attach_cleanup_error(exc, cleanup_error)
        return False


class SandboxFiles:
    def __init__(self, sandbox: Sandbox) -> None:
        self._sandbox = sandbox

    def write(self, path: str, data: str | bytes | IO[bytes] | Any) -> SandboxFileData:
        content = data.encode("utf-8") if isinstance(data, str) else data
        response = self._sandbox._api.files.upload(self._sandbox.sandbox_id, path=path, content=content)
        if response.data is None:
            raise _missing_data("file write", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data

    def read(self, path: str, *, format: Literal["text", "bytes"] = "text") -> str | bytes:
        if format not in {"text", "bytes"}:
            raise ValueError("format must be 'text' or 'bytes'")
        content = self._sandbox._api.files.download(self._sandbox.sandbox_id, path=path)
        return content.decode("utf-8") if format == "text" else content

    def remove(self, path: str) -> SandboxFileData:
        response = self._sandbox._api.files.delete(self._sandbox.sandbox_id, path=path)
        if response.data is None:
            raise _missing_data("file remove", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data

    def list(self, path: str | None = None, *, depth: int | None = None) -> List[SandboxEntryInfo]:
        response = self._sandbox._api.files.list(self._sandbox.sandbox_id, path=path, depth=depth)
        return response.data or []

    def stat(self, path: str | None = None) -> SandboxEntryInfo:
        response = self._sandbox._api.files.stat(self._sandbox.sandbox_id, path=path)
        if response.data is None:
            raise _missing_data("file stat", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data

    def rename(self, path: str, new_path: str) -> SandboxFileData:
        response = self._sandbox._api.files.move(self._sandbox.sandbox_id, path=path, new_path=new_path)
        if response.data is None:
            raise _missing_data("file rename", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data

    def make_dir(self, path: str) -> SandboxFileData:
        response = self._sandbox._api.files.make_directory(self._sandbox.sandbox_id, path=path)
        if response.data is None:
            raise _missing_data("make directory", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data


class AsyncSandboxFiles:
    def __init__(self, sandbox: AsyncSandbox) -> None:
        self._sandbox = sandbox

    async def write(self, path: str, data: str | bytes | IO[bytes] | Any) -> SandboxFileData:
        content = data.encode("utf-8") if isinstance(data, str) else data
        response = await self._sandbox._api.files.upload(self._sandbox.sandbox_id, path=path, content=content)
        if response.data is None:
            raise _missing_data("file write", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data

    async def read(self, path: str, *, format: Literal["text", "bytes"] = "text") -> str | bytes:
        if format not in {"text", "bytes"}:
            raise ValueError("format must be 'text' or 'bytes'")
        content = await self._sandbox._api.files.download(self._sandbox.sandbox_id, path=path)
        return content.decode("utf-8") if format == "text" else content

    async def remove(self, path: str) -> SandboxFileData:
        response = await self._sandbox._api.files.delete(self._sandbox.sandbox_id, path=path)
        if response.data is None:
            raise _missing_data("file remove", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data

    async def list(self, path: str | None = None, *, depth: int | None = None) -> List[SandboxEntryInfo]:
        response = await self._sandbox._api.files.list(self._sandbox.sandbox_id, path=path, depth=depth)
        return response.data or []

    async def stat(self, path: str | None = None) -> SandboxEntryInfo:
        response = await self._sandbox._api.files.stat(self._sandbox.sandbox_id, path=path)
        if response.data is None:
            raise _missing_data("file stat", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data

    async def rename(self, path: str, new_path: str) -> SandboxFileData:
        response = await self._sandbox._api.files.move(self._sandbox.sandbox_id, path=path, new_path=new_path)
        if response.data is None:
            raise _missing_data("file rename", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data

    async def make_dir(self, path: str) -> SandboxFileData:
        response = await self._sandbox._api.files.make_directory(self._sandbox.sandbox_id, path=path)
        if response.data is None:
            raise _missing_data("make directory", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data


class SandboxCommands:
    def __init__(self, sandbox: Sandbox) -> None:
        self._sandbox = sandbox

    def run(
        self,
        command: str,
        *,
        cwd: str | None = None,
        envs: Mapping[str, str] | None = None,
        timeout: int = 60,
        request_timeout: RequestTimeout = NOT_GIVEN,
    ) -> SandboxCommandResult:
        transport_timeout: RequestTimeout = (
            float(timeout + 30) if isinstance(request_timeout, NotGiven) else request_timeout
        )
        response = self._sandbox._api.commands.run(
            self._sandbox.sandbox_id,
            command,
            cwd=cwd,
            envs=envs,
            timeout_seconds=timeout,
            timeout=transport_timeout,
        )
        if response.data is None:
            raise _missing_data("command", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data


class AsyncSandboxCommands:
    def __init__(self, sandbox: AsyncSandbox) -> None:
        self._sandbox = sandbox

    async def run(
        self,
        command: str,
        *,
        cwd: str | None = None,
        envs: Mapping[str, str] | None = None,
        timeout: int = 60,
        request_timeout: RequestTimeout = NOT_GIVEN,
    ) -> SandboxCommandResult:
        transport_timeout: RequestTimeout = (
            float(timeout + 30) if isinstance(request_timeout, NotGiven) else request_timeout
        )
        response = await self._sandbox._api.commands.run(
            self._sandbox.sandbox_id,
            command,
            cwd=cwd,
            envs=envs,
            timeout_seconds=timeout,
            timeout=transport_timeout,
        )
        if response.data is None:
            raise _missing_data("command", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data


class SandboxPorts:
    def __init__(self, sandbox: Sandbox) -> None:
        self._sandbox = sandbox

    def open(self, port: int) -> SandboxPortInfo:
        response = self._sandbox._api.ports.open(self._sandbox.sandbox_id, port)
        if response.data is None:
            raise _missing_data("port open", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data

    def list(self) -> List[SandboxPortInfo]:
        response = self._sandbox._api.ports.list(self._sandbox.sandbox_id)
        return response.data or []

    def close(self, port: int) -> None:
        self._sandbox._api.ports.close(self._sandbox.sandbox_id, port)


class AsyncSandboxPorts:
    def __init__(self, sandbox: AsyncSandbox) -> None:
        self._sandbox = sandbox

    async def open(self, port: int) -> SandboxPortInfo:
        response = await self._sandbox._api.ports.open(self._sandbox.sandbox_id, port)
        if response.data is None:
            raise _missing_data("port open", self._sandbox.sandbox_id, self._sandbox.metadata)
        return response.data

    async def list(self) -> List[SandboxPortInfo]:
        response = await self._sandbox._api.ports.list(self._sandbox.sandbox_id)
        return response.data or []

    async def close(self, port: int) -> None:
        await self._sandbox._api.ports.close(self._sandbox.sandbox_id, port)


class SandboxProxy:
    def __init__(self, sandbox: Sandbox) -> None:
        self._sandbox = sandbox

    def request(
        self,
        method: str,
        path: str,
        *,
        query: Query | None = None,
        headers: Headers | None = None,
        json: Any = None,
        content: str | bytes | None = None,
        max_retries: int = 0,
        request_timeout: RequestTimeout = NOT_GIVEN,
    ) -> bytes:
        return self._sandbox._api.proxy.request(
            self._sandbox.sandbox_id,
            method,
            path,
            query=query,
            headers=headers,
            json=json,
            content=content,
            max_retries=max_retries,
            timeout=request_timeout,
        )


class AsyncSandboxProxy:
    def __init__(self, sandbox: AsyncSandbox) -> None:
        self._sandbox = sandbox

    async def request(
        self,
        method: str,
        path: str,
        *,
        query: Query | None = None,
        headers: Headers | None = None,
        json: Any = None,
        content: str | bytes | None = None,
        max_retries: int = 0,
        request_timeout: RequestTimeout = NOT_GIVEN,
    ) -> bytes:
        return await self._sandbox._api.proxy.request(
            self._sandbox.sandbox_id,
            method,
            path,
            query=query,
            headers=headers,
            json=json,
            content=content,
            max_retries=max_retries,
            timeout=request_timeout,
        )


class SandboxResourceWithRawResponse:
    def __init__(self, sandbox: SandboxResource) -> None:
        self._sandbox = sandbox

    @cached_property
    def api(self) -> SandboxAPIResourceWithRawResponse:
        return SandboxAPIResourceWithRawResponse(self._sandbox.api)


class AsyncSandboxResourceWithRawResponse:
    def __init__(self, sandbox: AsyncSandboxResource) -> None:
        self._sandbox = sandbox

    @cached_property
    def api(self) -> AsyncSandboxAPIResourceWithRawResponse:
        return AsyncSandboxAPIResourceWithRawResponse(self._sandbox.api)


class SandboxResourceWithStreamingResponse:
    def __init__(self, sandbox: SandboxResource) -> None:
        self._sandbox = sandbox

    @cached_property
    def api(self) -> SandboxAPIResourceWithStreamingResponse:
        return SandboxAPIResourceWithStreamingResponse(self._sandbox.api)


class AsyncSandboxResourceWithStreamingResponse:
    def __init__(self, sandbox: AsyncSandboxResource) -> None:
        self._sandbox = sandbox

    @cached_property
    def api(self) -> AsyncSandboxAPIResourceWithStreamingResponse:
        return AsyncSandboxAPIResourceWithStreamingResponse(self._sandbox.api)
