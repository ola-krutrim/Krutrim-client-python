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

COPY --from=agent-build /out/sandbox-agent /usr/local/bin/sandbox-agent

RUN chown -R 1000:1000 /app
USER 1000

EXPOSE 8871
CMD ["sandbox-agent"]
