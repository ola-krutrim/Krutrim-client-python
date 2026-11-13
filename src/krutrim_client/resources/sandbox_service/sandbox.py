from __future__ import annotations

from .files import (
    FilesResource,
    AsyncFilesResource,
    FilesResourceWithRawResponse,
    AsyncFilesResourceWithRawResponse,
    FilesResourceWithStreamingResponse,
    AsyncFilesResourceWithStreamingResponse,
)
from .ports import (
    PortsResource,
    AsyncPortsResource,
    PortsResourceWithRawResponse,
    AsyncPortsResourceWithRawResponse,
    PortsResourceWithStreamingResponse,
    AsyncPortsResourceWithStreamingResponse,
)
from .flavors import (
    FlavorsResource,
    AsyncFlavorsResource,
    FlavorsResourceWithRawResponse,
    AsyncFlavorsResourceWithRawResponse,
    FlavorsResourceWithStreamingResponse,
    AsyncFlavorsResourceWithStreamingResponse,
)
from .network import (
    NetworkResource,
    AsyncNetworkResource,
    NetworkResourceWithRawResponse,
    AsyncNetworkResourceWithRawResponse,
    NetworkResourceWithStreamingResponse,
    AsyncNetworkResourceWithStreamingResponse,
)
from .commands import (
    CommandsResource,
    AsyncCommandsResource,
    CommandsResourceWithRawResponse,
    AsyncCommandsResourceWithRawResponse,
    CommandsResourceWithStreamingResponse,
    AsyncCommandsResourceWithStreamingResponse,
)
from .terminal import (
    TerminalResource,
    AsyncTerminalResource,
    TerminalResourceWithRawResponse,
    AsyncTerminalResourceWithRawResponse,
    TerminalResourceWithStreamingResponse,
    AsyncTerminalResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .sandboxes import (
    SandboxesResource,
    AsyncSandboxesResource,
    SandboxesResourceWithRawResponse,
    AsyncSandboxesResourceWithRawResponse,
    SandboxesResourceWithStreamingResponse,
    AsyncSandboxesResourceWithStreamingResponse,
)
from .templates import (
    TemplatesResource,
    AsyncTemplatesResource,
    TemplatesResourceWithRawResponse,
    AsyncTemplatesResourceWithRawResponse,
    TemplatesResourceWithStreamingResponse,
    AsyncTemplatesResourceWithStreamingResponse,
)
from .operations import (
    OperationsResource,
    AsyncOperationsResource,
    OperationsResourceWithRawResponse,
    AsyncOperationsResourceWithRawResponse,
    OperationsResourceWithStreamingResponse,
    AsyncOperationsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource


class SandboxResource(SyncAPIResource):
    @cached_property
    def sandboxes(self) -> SandboxesResource:
        return SandboxesResource(self._client)

    @cached_property
    def templates(self) -> TemplatesResource:
        return TemplatesResource(self._client)

    @cached_property
    def flavors(self) -> FlavorsResource:
        return FlavorsResource(self._client)

    @cached_property
    def operations(self) -> OperationsResource:
        return OperationsResource(self._client)

    @cached_property
    def commands(self) -> CommandsResource:
        return CommandsResource(self._client)

    @cached_property
    def files(self) -> FilesResource:
        return FilesResource(self._client)

    @cached_property
    def network(self) -> NetworkResource:
        return NetworkResource(self._client)

    @cached_property
    def ports(self) -> PortsResource:
        return PortsResource(self._client)

    @cached_property
    def terminal(self) -> TerminalResource:
        return TerminalResource(self._client)

    @cached_property
    def with_raw_response(self) -> SandboxResourceWithRawResponse:
        return SandboxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SandboxResourceWithStreamingResponse:
        return SandboxResourceWithStreamingResponse(self)


class SandboxResourceWithRawResponse:
    def __init__(self, resource: SandboxResource) -> None:
        self.sandboxes = SandboxesResourceWithRawResponse(resource.sandboxes)
        self.templates = TemplatesResourceWithRawResponse(resource.templates)
        self.flavors = FlavorsResourceWithRawResponse(resource.flavors)
        self.operations = OperationsResourceWithRawResponse(resource.operations)
        self.commands = CommandsResourceWithRawResponse(resource.commands)
        self.files = FilesResourceWithRawResponse(resource.files)
        self.network = NetworkResourceWithRawResponse(resource.network)
        self.ports = PortsResourceWithRawResponse(resource.ports)
        self.terminal = TerminalResourceWithRawResponse(resource.terminal)


class SandboxResourceWithStreamingResponse:
    def __init__(self, resource: SandboxResource) -> None:
        self.sandboxes = SandboxesResourceWithStreamingResponse(resource.sandboxes)
        self.templates = TemplatesResourceWithStreamingResponse(resource.templates)
        self.flavors = FlavorsResourceWithStreamingResponse(resource.flavors)
        self.operations = OperationsResourceWithStreamingResponse(resource.operations)
        self.commands = CommandsResourceWithStreamingResponse(resource.commands)
        self.files = FilesResourceWithStreamingResponse(resource.files)
        self.network = NetworkResourceWithStreamingResponse(resource.network)
        self.ports = PortsResourceWithStreamingResponse(resource.ports)
        self.terminal = TerminalResourceWithStreamingResponse(resource.terminal)


class AsyncSandboxResource(AsyncAPIResource):
    @cached_property
    def sandboxes(self) -> AsyncSandboxesResource:
        return AsyncSandboxesResource(self._client)

    @cached_property
    def templates(self) -> AsyncTemplatesResource:
        return AsyncTemplatesResource(self._client)

    @cached_property
    def flavors(self) -> AsyncFlavorsResource:
        return AsyncFlavorsResource(self._client)

    @cached_property
    def operations(self) -> AsyncOperationsResource:
        return AsyncOperationsResource(self._client)

    @cached_property
    def commands(self) -> AsyncCommandsResource:
        return AsyncCommandsResource(self._client)

    @cached_property
    def files(self) -> AsyncFilesResource:
        return AsyncFilesResource(self._client)

    @cached_property
    def network(self) -> AsyncNetworkResource:
        return AsyncNetworkResource(self._client)

    @cached_property
    def ports(self) -> AsyncPortsResource:
        return AsyncPortsResource(self._client)

    @cached_property
    def terminal(self) -> AsyncTerminalResource:
        return AsyncTerminalResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSandboxResourceWithRawResponse:
        return AsyncSandboxResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSandboxResourceWithStreamingResponse:
        return AsyncSandboxResourceWithStreamingResponse(self)


class AsyncSandboxResourceWithRawResponse:
    def __init__(self, resource: AsyncSandboxResource) -> None:
        self.sandboxes = AsyncSandboxesResourceWithRawResponse(resource.sandboxes)
        self.templates = AsyncTemplatesResourceWithRawResponse(resource.templates)
        self.flavors = AsyncFlavorsResourceWithRawResponse(resource.flavors)
        self.operations = AsyncOperationsResourceWithRawResponse(resource.operations)
        self.commands = AsyncCommandsResourceWithRawResponse(resource.commands)
        self.files = AsyncFilesResourceWithRawResponse(resource.files)
        self.network = AsyncNetworkResourceWithRawResponse(resource.network)
        self.ports = AsyncPortsResourceWithRawResponse(resource.ports)
        self.terminal = AsyncTerminalResourceWithRawResponse(resource.terminal)


class AsyncSandboxResourceWithStreamingResponse:
    def __init__(self, resource: AsyncSandboxResource) -> None:
        self.sandboxes = AsyncSandboxesResourceWithStreamingResponse(resource.sandboxes)
        self.templates = AsyncTemplatesResourceWithStreamingResponse(resource.templates)
        self.flavors = AsyncFlavorsResourceWithStreamingResponse(resource.flavors)
        self.operations = AsyncOperationsResourceWithStreamingResponse(resource.operations)
        self.commands = AsyncCommandsResourceWithStreamingResponse(resource.commands)
        self.files = AsyncFilesResourceWithStreamingResponse(resource.files)
        self.network = AsyncNetworkResourceWithStreamingResponse(resource.network)
        self.ports = AsyncPortsResourceWithStreamingResponse(resource.ports)
        self.terminal = AsyncTerminalResourceWithStreamingResponse(resource.terminal)
