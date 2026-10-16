# Krutrim Sandbox template — PHP
#
# PHP CLI with Composer and common extensions.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       php-cli php-mbstring php-xml php-curl php-zip composer \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R 1000:1000 /app
USER 1000
