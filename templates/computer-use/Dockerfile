# Krutrim Sandbox template — computer use
#
# Xvfb plus a real Chromium, so an agent can drive a browser inside a sandbox.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).
#
# NOTE: Ubuntu's apt `chromium-browser` is a snap shim and CANNOT work in a
# container — it only prints "requires the chromium snap to be installed", and
# snap needs systemd. Xvfb itself is fine. We install Playwright's bundled
# Chromium, which is a real binary.
#
# Verified on sandbox-large, In-Bangalore-1: real Chromium under gVisor,
# <title>Example Domain</title> in 2.9s with no runtime install.

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       xvfb x11-utils xauth fonts-liberation fonts-noto-color-emoji \
       libnss3 libnspr4 libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 \
       libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
       libgbm1 libpango-1.0-0 libcairo2 libasound2t64 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir requests==2.32.5 playwright==1.64.0

# Chromium must land somewhere UID 1000 can read. Install it as that user.
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright
RUN mkdir -p /opt/playwright && chown -R 1000:1000 /opt/playwright
USER 1000
RUN python3 -m playwright install chromium
USER root

# Helper: bring up a display, then run anything that needs one.
#   with-display chromium --headless=new --dump-dom https://example.com
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
