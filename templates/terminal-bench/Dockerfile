# Krutrim Sandbox template — terminal bench
#
# Terminal tooling for agent benchmarking and recorded sessions.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       tmux asciinema expect jq ripgrep fd-find bat tree htop \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R 1000:1000 /app
USER 1000
