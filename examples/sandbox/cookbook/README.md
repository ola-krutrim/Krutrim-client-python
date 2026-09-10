# Omni Sandbox Cookbook

Task-oriented recipes for the sandbox SDK. Each recipe lives in its own
directory with a README covering setup, walkthrough, and expected output.
New to the sandbox? Start with [`basic/`](basic/).

| Recipe | What it shows |
| --- | --- |
| [`basic/`](basic/) | Create a sandbox, upload a program, run it, and read the result back — sync and async variants |
| [`web_service_ports_proxy/`](web_service_ports_proxy/) | Run an HTTP service in a sandbox; open a port, call it via the authenticated `sandbox.proxy`, and share its public URL |
| [`data_pipeline_csv/`](data_pipeline_csv/) | Upload a CSV, transform it in-sandbox, inspect with `files.list`/`stat`, download results as text and exact bytes |
| [`parallel_sandboxes_async/`](parallel_sandboxes_async/) | Fan chunks out to concurrent sandboxes with `AsyncKrutrimClient` + `asyncio.gather` and aggregate the results |
