from __future__ import annotations

import pytest

from krutrim_client import KrutrimClient, AsyncKrutrimClient
from krutrim_client._models import FinalRequestOptions

BASE_URL = "http://127.0.0.1:4010"
API_KEY = "test-api-key"


@pytest.mark.parametrize("content", [b"sandbox payload", b""])
def test_sync_build_request_preserves_raw_content(content: bytes) -> None:
    with KrutrimClient(base_url=BASE_URL, api_key=API_KEY) as client:
        request = client._build_request(
            FinalRequestOptions(method="post", url="/raw", content=content),
        )

    assert request.content == content


@pytest.mark.parametrize("content", [b"sandbox payload", b""])
async def test_async_build_request_preserves_raw_content(content: bytes) -> None:
    async with AsyncKrutrimClient(base_url=BASE_URL, api_key=API_KEY) as client:
        request = client._build_request(
            FinalRequestOptions(method="post", url="/raw", content=content),
        )

    assert request.content == content


@pytest.mark.parametrize(
    "other_body",
    [
        {"json_data": {"kind": "json"}},
        {"extra_json": {"kind": "extra-json"}},
        {"files": {"file": ("payload.bin", b"payload")}},
    ],
)
def test_sync_build_request_rejects_ambiguous_raw_content(other_body: dict[str, object]) -> None:
    with KrutrimClient(base_url=BASE_URL, api_key=API_KEY) as client:
        options = FinalRequestOptions.construct(
            method="post",
            url="/raw",
            content=b"payload",
            **other_body,  # type: ignore[arg-type]
        )

        with pytest.raises(ValueError, match="raw content"):
            client._build_request(options)


@pytest.mark.parametrize(
    "other_body",
    [
        {"json_data": {"kind": "json"}},
        {"extra_json": {"kind": "extra-json"}},
        {"files": {"file": ("payload.bin", b"payload")}},
    ],
)
async def test_async_build_request_rejects_ambiguous_raw_content(other_body: dict[str, object]) -> None:
    async with AsyncKrutrimClient(base_url=BASE_URL, api_key=API_KEY) as client:
        options = FinalRequestOptions.construct(
            method="post",
            url="/raw",
            content=b"payload",
            **other_body,  # type: ignore[arg-type]
        )

        with pytest.raises(ValueError, match="raw content"):
            client._build_request(options)
