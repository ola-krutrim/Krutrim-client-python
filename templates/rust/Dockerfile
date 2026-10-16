# Krutrim Sandbox template — Rust
#
# The Rust toolchain via rustup.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

ENV RUSTUP_HOME=/opt/rustup CARGO_HOME=/opt/cargo
ENV PATH=/opt/cargo/bin:${PATH}
RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --no-modify-path --profile minimal \
    && chmod -R a+rwX /opt/cargo /opt/rustup

RUN chown -R 1000:1000 /app
USER 1000
