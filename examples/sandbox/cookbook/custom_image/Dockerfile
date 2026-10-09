FROM golang:1.24 AS agent-build
WORKDIR /src
COPY agent/ .
RUN CGO_ENABLED=0 go build -trimpath -ldflags='-s -w' -o /out/sandbox-agent .

FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv libgomp1 git curl iproute2 net-tools lsof \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir requests==2.32.5
ENV PATH=/opt/venv/bin:${PATH}

COPY --from=agent-build /out/sandbox-agent /usr/local/bin/sandbox-agent

RUN chown -R 1000:1000 /app
USER 1000

EXPOSE 8871

CMD ["sandbox-agent"]
