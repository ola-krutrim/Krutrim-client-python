# Krutrim Sandbox template — media processing
#
# ffmpeg and image tooling for audio, video and image work.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ffmpeg imagemagick libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pillow imageio imageio-ffmpeg

RUN chown -R 1000:1000 /app
USER 1000
