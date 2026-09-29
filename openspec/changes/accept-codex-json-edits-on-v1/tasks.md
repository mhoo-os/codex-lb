## 1. Reproduce and repair
- [x] Reproduce the JSON request failure at the public route using a fake upstream.
- [x] Reuse the native JSON edit handler for application/json public requests.
- [x] Preserve generic JSON request-size admission and multipart behavior.

## 2. Verify
- [x] Verify round trip, malformed inputs, authorization, size limits and multipart regression tests.
- [x] Run source lint/type checks and strict OpenSpec validation.
- [x] Record exact source, patch and proof limits; leave deployment/client configuration unchanged.

Local results: image-route and multipart middleware suite 117 passed; final changed-test subset 14 passed; supporting schema/translation/body-limit/decompression suite 179 passed. Ruff, formatting, ty and architecture checks passed. Strict change validation passed. Global strict spec validation reports 35 passed / 22 failed in unchanged baseline specs (placeholder purposes); archive is deferred until required verification/review gates are resolved. No current-head remote CI, review or live-recovery claim.
