# Krutrim Sandbox template — Hermes Agent
#
# Nous Research's open-source Hermes Agent (MIT, github.com/NousResearch/hermes-agent).
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).
#
# From PyPI rather than upstream's install.sh. Both were measured in a sandbox first:
#
#   pip install hermes-agent==0.19.0    41 s   189 MB   v0.19.0, --version and --help ok
#   official install.sh                750 s   2.7 GB   v0.22.2, own Python 3.14
#
# The installer stages its own Python 3.14 plus 58 bundled skills, hence 2.7 GB. It
# also publishes the launcher under /root/.local/bin — out of reach once the image
# drops to UID 1000 — appends to shell rc files, and enables a background skill
# curator, none of which suits an ephemeral sandbox image. Its cua-driver step
# additionally failed here on a missing libX11.so.6.
#
# The cost is version lag: PyPI carries 0.19.0 while the repo is at v0.22.2.
# `hermes update` moves a running sandbox forward. Upstream's .python-version says
# 3.14 and this base ships Ubuntu 24.04's 3.12; the package declares >=3.11,<3.15
# and was exercised on 3.12 before this was committed.

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN pip install --no-cache-dir hermes-agent==0.19.0

# Hermes keeps state under HERMES_HOME, defaulting to $HOME/.hermes. Both resolutions
# work here — ubuntu:24.04 carries ubuntu:x:1000:1000 with /home/ubuntu mode 750 — but
# they differ: state lands in /root/.hermes when the platform starts the container as
# root (it currently does, despite USER 1000) and in /home/ubuntu/.hermes when it
# honours the contract. Naming the directory makes that one path either way.
#
# This is not optional hygiene for an arbitrary UID. Measured: run the CLI as a UID
# with no passwd entry and it dies at import with exit 120, inside
# hermes_constants._get_platform_default_hermes_home, and HERMES_HOME does not rescue
# it — the crash happens before the override is read. Any future runtime that assigns
# containers an unmapped UID breaks this template.
ENV HERMES_HOME=/opt/hermes-home
RUN mkdir -p /opt/hermes-home && chown -R 1000:1000 /opt/hermes-home

RUN chown -R 1000:1000 /app
USER 1000
