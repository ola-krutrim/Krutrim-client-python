# Krutrim Sandbox template — Aider
#
# The Aider pair-programming agent.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN pip install --no-cache-dir aider-chat

RUN chown -R 1000:1000 /app
USER 1000
