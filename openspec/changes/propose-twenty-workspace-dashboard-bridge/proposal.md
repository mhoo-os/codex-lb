## Why

Mhoo needs a native Twenty surface for aggregate Codex-LB cost and usage across
its Workspaces. Twenty remains the authority for people, roles, and Workspace
UI; Codex-LB remains the authority for routing and operational telemetry. The
browser must not receive a Codex-LB credential or reuse the privileged
Codex-LB dashboard.

## What Changes

- Add an optional one-to-one Twenty Workspace attribution to dedicated proxy
  API keys.
- Add a disabled-by-default, versioned, read-only aggregate usage endpoint for
  a dedicated Twenty App service identity.
- Return only fixed aggregate request, token, cached-token, error, cost, and
  per-model fields for `1d`, `7d`, or `30d` windows.
- Authenticate with one distinct server-side bearer credential, whose presence
  enables the otherwise absent route, rate-limit valid
  reads, and audit successful reads without logging secrets.
- Keep iframe embedding out of the first implementation.

## Capabilities

### New Capabilities

- `twenty-workspace-dashboard-bridge`: privacy-bounded aggregate telemetry for
  the owner-only native Twenty App.

### Modified Capabilities

None.

## Impact

This change adds a database migration, optional API-key attribution fields,
configuration validation, one read-only integration route, and tests. The
route is absent at runtime unless a separate bridge token is provisioned. It
does not install the Twenty App, bind a live key, provision a secret,
or enable production; those remain cross-repository deployment gates.
