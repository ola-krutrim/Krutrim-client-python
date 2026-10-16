# Krutrim Sandbox template — Go
#
# The Go toolchain.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

ENV PATH=/usr/local/go/bin:${PATH}
ENV GOPATH=/app/go
RUN curl -fsSL https://go.dev/dl/go1.24.8.linux-amd64.tar.gz -o /tmp/go.tgz \
    && tar -C /usr/local -xzf /tmp/go.tgz && rm /tmp/go.tgz

RUN chown -R 1000:1000 /app
USER 1000
