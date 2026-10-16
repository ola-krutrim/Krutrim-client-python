# Krutrim Sandbox template — data science
#
# Heavier analytics stack: scikit-learn, scipy, polars, duckdb.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libgomp1 libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir numpy pandas scipy scikit-learn polars duckdb pyarrow \
        matplotlib seaborn statsmodels

RUN chown -R 1000:1000 /app
USER 1000
