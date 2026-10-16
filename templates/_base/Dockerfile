# Krutrim Sandbox template base
#
# Every template builds FROM this. It carries the BYOC contract — the agent,
# port 8871, /app owned by UID 1000 — so a template only adds its own tools.
#
# Build context is the repository root, so the agent comes from the cookbook
# rather than a copy that would drift.

FROM golang:1.24 AS agent-build
WORKDIR /src
COPY examples/sandbox/cookbook/custom_image/agent/ .
RUN CGO_ENABLED=0 go build -trimpath -ldflags='-s -w' -o /out/sandbox-agent .

FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3 python3-pip python3-venv libgomp1 \
       git curl wget ca-certificates unzip xz-utils \
       iproute2 net-tools lsof procps tini \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH=/opt/venv/bin:${PATH}

# Name HOME so nothing has to resolve it through getpwuid(). Measured: a UID with
# no /etc/passwd entry and HOME unset makes tools that expand ~ fail at import —
# Hermes raises RuntimeError: Could not determine home directory. Setting HOME
# alone fixes it; a tool-specific override such as HERMES_HOME does not, because
# the lookup happens before the override is read. ubuntu:24.04 does carry
# ubuntu:x:1000:1000 with /home/ubuntu, so UID 1000 works without this, but the
# platform starts containers as root today and may assign an unmapped UID later.
ENV HOME=/app

COPY --from=agent-build /out/sandbox-agent /usr/local/bin/sandbox-agent

RUN chown -R 1000:1000 /app
USER 1000

EXPOSE 8871
CMD ["sandbox-agent"]
