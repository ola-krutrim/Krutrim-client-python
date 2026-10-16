# Krutrim Sandbox template — Java
#
# Temurin JDK 21 with Maven and Gradle.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       openjdk-21-jdk-headless maven gradle \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R 1000:1000 /app
USER 1000
