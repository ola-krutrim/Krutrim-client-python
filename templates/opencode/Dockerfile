# Krutrim Sandbox template — OpenCode
#
# The OpenCode agent CLI.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g opencode-ai \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R 1000:1000 /app
USER 1000
