# JSON reference compatibility

Codex clients using a `/v1` base URL can send a valid JSON prompt and data-URL reference to a multipart-only handler. Multipart validation then reports a missing prompt. The native Codex edit handler already supports this JSON format; content-type dispatch reuses it without duplicating decoding, model policy or the provider pipeline.

For example, `{"model":"gpt-image-2","prompt":"make it green","images":[{"image_url":"data:image/png;base64,..."}]}` now reaches the same handler on both edit routes. Multipart SDK uploads retain their existing path.

JSON requests use generic raw/decompressed body admission, like the native route. Declared oversize bodies may return 413 before route authorization. Content-encoded JSON is bounded and decoded by existing generic middleware before route authorization; unencoded JSON authorization does not consume the body. Multipart admission and auth-first handling are unchanged.

Local fake-upstream tests establish source behavior only. They do not identify the deployed version or prove live image-tool recovery. Publication, current-head CI/review and infrastructure-owned rollout remain separate steps.

## Merge prerequisites

The owner requested merge and deployment after the initial draft. CI revealed existing contributor-attribution drift and CVE-2026-63374 in AnyIO 4.13.0. Refresh the generated contributor list and lock AnyIO to the scanner-reported fixed 4.14.2 release; keep the image-edit implementation unchanged. Re-run the affected runtime checks and current-head CI before merge.
