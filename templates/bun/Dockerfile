# Krutrim Sandbox template — Bun
#
# The Bun runtime and package manager.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

ENV BUN_INSTALL=/opt/bun
ENV PATH=/opt/bun/bin:${PATH}
RUN curl -fsSL https://bun.sh/install | bash && chmod -R a+rx /opt/bun

RUN chown -R 1000:1000 /app
USER 1000
