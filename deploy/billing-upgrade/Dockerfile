FROM oven/bun:1.4.2-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/bun.lock ./
RUN bun install --frozen-lockfile
COPY frontend ./
RUN bun run build
FROM ghcr.io/mhoo-os/codex-lb@sha256:8774e4606997ffe51ffba4122d35be759e5d75795cacd4324ddf65fb68ea330c
COPY --chown=app:app app /app/app
COPY --chown=app:app --from=frontend-build /app/app/static /app/app/static
ARG SOURCE_REVISION
LABEL org.opencontainers.image.revision=$SOURCE_REVISION org.opencontainers.image.source="https://github.com/mhoo-os/codex-lb"
