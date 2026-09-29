## Why

Codex clients configured with a `/v1` base URL submit reference-image edits as JSON with data-URL images. The public edit route currently expects multipart, so a valid JSON prompt is reported missing. The native Codex alias already parses this format.

## What Changes

- Dispatch JSON edit requests on `/v1/images/edits` through the existing native JSON handler.
- Keep multipart SDK requests and existing authentication, model policy, limits and settlement behavior.
- Keep JSON bodies under generic raw/decompressed admission, including identity/compressed requests.
- Cover both routes with round-trip and invalid-input regressions; preserve multipart and authorization regressions.

## Impact

ARCHITECTURE IMPACT: LOCAL. Reuses the existing edit pipeline. No provider, credential, model, configuration or deployment change. This is a locally prepared compatibility repair, not proof of a deployed fix.
