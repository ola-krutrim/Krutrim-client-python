# Krutrim Sandbox template — computer use
#
# Verified working on sandbox-large (2 vCPU / 4 GB), In-Bangalore-1, 2026-10-16:
#   real Chromium launched under gVisor, navigated, screenshotted.
#   Doing this at runtime costs ~100s and ~310 MB on every create; baking removes it.
#
# NOTE: Ubuntu's apt `chromium-browser` is a snap shim and CANNOT work in a
# container — it only prints "requires the chromium snap to be installed".
# We install Playwright's bundled Chromium, which is a real binary.
#
# Build:  docker build --platform linux/amd64 -t ghcr.io/<org>/sandbox-computer-use:v1 .
# Limits: linux/amd64 manifest, <= 4 GiB compressed, public registry.

FROM golang:1.24 AS agent-build
WORKDIR /src
COPY examples/sandbox/cookbook/custom_image/agent/ .
RUN CGO_ENABLED=0 go build -trimpath -ldflags='-s -w' -o /out/sandbox-agent .

FROM ubuntu:24.04

WORKDIR /app

# Base runtime (mirrors the cookbook) plus the X stack and Chromium's shared libs.
# xvfb + x11-utils give a working display; the rest are Chromium's runtime deps.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3 python3-pip python3-venv libgomp1 git curl iproute2 net-tools lsof \
       xvfb x11-utils xauth fonts-liberation fonts-noto-color-emoji \
       libnss3 libnspr4 libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 \
       libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
       libgbm1 libpango-1.0-0 libcairo2 libasound2t64 \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir requests==2.32.5 playwright==1.64.0
ENV PATH=/opt/venv/bin:${PATH}

# Chromium must land somewhere UID 1000 can read. Install it as that user.
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright
RUN mkdir -p /opt/playwright && chown -R 1000:1000 /opt/playwright
USER 1000
RUN python3 -m playwright install chromium
USER root

COPY --from=agent-build /out/sandbox-agent /usr/local/bin/sandbox-agent

# Helper: bring up a display, then run anything that needs one.
#   with-display chromium-headless-shell --dump-dom https://example.com
RUN printf '%s\n' \
    '#!/bin/sh' \
    '# Start Xvfb on :99 if nothing is there yet, then exec the given command.' \
    'if ! xdpyinfo -display :99 >/dev/null 2>&1; then' \
    '  Xvfb :99 -screen 0 1280x800x24 >/tmp/xvfb.log 2>&1 &' \
    '  for i in $(seq 1 40); do xdpyinfo -display :99 >/dev/null 2>&1 && break; sleep 0.25; done' \
    'fi' \
    'DISPLAY=:99 exec "$@"' \
    > /usr/local/bin/with-display \
    && chmod 0755 /usr/local/bin/with-display

RUN chown -R 1000:1000 /app
USER 1000

# The agent is the entrypoint. Xvfb and the browser start on demand, per the
# cookbook's guidance that application services run separately from the agent.
EXPOSE 8871
CMD ["sandbox-agent"]
