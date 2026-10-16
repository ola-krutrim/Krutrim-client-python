# Krutrim Sandbox template — code interpreter
#
# Python with the standard data stack and Jupyter, for code-execution agents.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN pip install --no-cache-dir jupyter-client ipykernel pandas numpy matplotlib tabulate \
        openpyxl pillow requests
RUN python3 -m ipykernel install --name krutrim --display-name 'Krutrim Sandbox'

RUN chown -R 1000:1000 /app
USER 1000
