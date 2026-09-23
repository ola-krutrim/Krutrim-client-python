from __future__ import annotations

import krutrim_client
from krutrim_client.resources.lb import HighlvlResource


def test_resources_proxy_resolves_actual_module() -> None:
    """Regression test for the `krutrimClient` vs `krutrim_client` typo in
    `_utils/_resources_proxy.py`.

    This must exercise the lazily-loaded attribute path (`krutrim_client.resources`)
    rather than just checking the import string, otherwise a broken module name
    passed to `importlib.import_module` would go undetected.
    """
    resources_module = krutrim_client.resources

    assert resources_module.__name__ == "krutrim_client.resources"
    # Accessing a real resource attribute forces full resolution of the proxy.
    assert resources_module.lb.HighlvlResource is HighlvlResource
