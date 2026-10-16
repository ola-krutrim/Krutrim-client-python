# Krutrim Sandbox template — Deno
#
# The Deno runtime.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

ENV DENO_INSTALL=/opt/deno
ENV PATH=/opt/deno/bin:${PATH}
RUN curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/opt/deno sh -s -- -y \
    && chmod -R a+rx /opt/deno

RUN chown -R 1000:1000 /app
USER 1000
