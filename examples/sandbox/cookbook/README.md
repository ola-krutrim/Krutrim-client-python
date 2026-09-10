# Omni Sandbox Cookbook

Task-oriented recipes for the sandbox SDK. Each recipe lives in its own
directory with a `main.py` and a README covering setup, walkthrough, and
expected output.

| Recipe | What it shows |
| --- | --- |
| [`web_service_ports_proxy/`](web_service_ports_proxy/) | Run an HTTP service in a sandbox; open a port, call it via the authenticated `sandbox.proxy`, and share its public URL |
| [`data_pipeline_csv/`](data_pipeline_csv/) | Upload a CSV, transform it in-sandbox, inspect with `files.list`/`stat`, download results as text and exact bytes |
| [`parallel_sandboxes_async/`](parallel_sandboxes_async/) | Fan chunks out to concurrent sandboxes with `AsyncKrutrimClient` + `asyncio.gather` and aggregate the results |
| [`lifecycle_and_ttl/`](lifecycle_and_ttl/) | Discover flavors/templates, create without a context manager, reattach with `connect`, extend TTL, delete explicitly |
