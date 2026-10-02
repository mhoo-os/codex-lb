FROM ghcr.io/mhoo-os/codex-lb@sha256:3ff0a2a27750e50e9aec6020050505719f9f4375259e62f1525d6d15edc9a6be
COPY --chown=app:app app/core/clients/proxy_websocket.py /app/app/core/clients/proxy_websocket.py
ARG SOURCE_REVISION
LABEL org.opencontainers.image.source="https://github.com/mhoo-os/codex-lb" \
      org.opencontainers.image.revision=$SOURCE_REVISION \
      mhoo.patch="native-receive-diagnostics-20261002"
