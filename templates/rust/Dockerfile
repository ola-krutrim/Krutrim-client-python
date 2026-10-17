# Krutrim Sandbox template — Rust
#
# The Rust toolchain via rustup.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

# rustup installs the compiler, not a linker. Without a C toolchain `rustc` reports its
# version happily and `cargo build` dies with "linker `cc` not found", producing no
# binary at all — a working version string on a toolchain that cannot build. Measured
# in a live sandbox on template-v1.2.0: cc, gcc, clang, ld and musl-gcc were all absent.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV RUSTUP_HOME=/opt/rustup CARGO_HOME=/opt/cargo
ENV PATH=/opt/cargo/bin:${PATH}
RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --no-modify-path --profile minimal \
    && chmod -R a+rwX /opt/cargo /opt/rustup

RUN chown -R 1000:1000 /app
USER 1000
