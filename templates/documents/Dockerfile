# Krutrim Sandbox template — documents
#
# Pandoc and LaTeX for document conversion and PDF rendering.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       pandoc texlive-latex-recommended texlive-fonts-recommended \
       texlive-latex-extra librsvg2-bin \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pypdf python-docx openpyxl markdown

RUN chown -R 1000:1000 /app
USER 1000
