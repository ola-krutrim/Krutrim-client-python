# Krutrim Sandbox template — Playwright browsers
#
# Playwright with Chromium, Firefox and WebKit for browser automation.
# Builds on sandbox-base, which carries the BYOC contract (agent, 8871, /app, UID 1000).

ARG BASE_TAG=latest
FROM ghcr.io/ola-krutrim/sandbox-base:${BASE_TAG}

USER root

RUN pip install --no-cache-dir playwright==1.64.0
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright
RUN mkdir -p /opt/playwright && chown -R 1000:1000 /opt/playwright
RUN python3 -m playwright install-deps
USER 1000
RUN python3 -m playwright install chromium firefox webkit
USER root

RUN chown -R 1000:1000 /app
USER 1000
