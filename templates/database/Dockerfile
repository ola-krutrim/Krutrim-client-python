# Krutrim Sandbox template — databases
#
# PostgreSQL, SQLite and Redis running locally in the sandbox.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       postgresql postgresql-client sqlite3 redis-server \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir psycopg2-binary redis sqlalchemy

RUN chown -R 1000:1000 /app
USER 1000
