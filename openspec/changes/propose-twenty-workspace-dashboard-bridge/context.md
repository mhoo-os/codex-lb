# Twenty Workspace dashboard bridge context

## Authority and data flow

Twenty owns user authentication, full-server-admin status, Workspace lifecycle,
and the UI. Codex-LB owns proxy keys and their operational telemetry. The
native path is:

```text
Twenty full server admin
  -> native Twenty front component
  -> authenticated Twenty App function
  -> dedicated bridge bearer credential
  -> Codex-LB aggregate usage API
```

The Twenty App checks `canAccessFullAdminPanel` both when deciding whether to
show its command and again in its server-side function. Codex-LB authenticates
the App service identity; it does not accept a Workspace ID, user ID, host, or
origin as authority.

## Workspace attribution

Each dedicated proxy key may carry one `twenty_workspace_id` and optional
display name. A database uniqueness constraint prevents two keys from claiming
the same Workspace. The mapping is attribution only: it does not authenticate
requests or grant access. Unbound keys are deliberately absent from the bridge
response.

Example: a proxy key named `mhoo-twenty-workspace` is bound to the immutable
Twenty Workspace ID and display name `MHOO`. Requests authenticated by that
key roll up under the MHOO row in the owner view.

## Privacy and retention

The response includes aggregate request counts, input/output/cached token
counts, non-success counts, persisted cost, last-use time, active state, and
per-model aggregates. It never includes key IDs or prefixes, credentials,
accounts, request IDs, client IPs, bodies, prompts, outputs, error messages, or
conversation identifiers. Warm-up requests are excluded.

The route reads Codex-LB's retained request-log data and does not copy telemetry
into Twenty objects. Existing Codex-LB retention therefore bounds the
available historical detail.

## Service identity and failure behavior

The route is disabled while `CODEX_LB_TWENTY_USAGE_BRIDGE_TOKEN` is absent.
Provisioning a distinct token of at least 32 characters enables it; an explicit
second enable flag is intentionally avoided. Authentication uses constant-time
comparison. A valid identity is limited to 120 reads per minute and successful
reads emit a `twenty_usage_bridge_read` audit event containing only the window
and Workspace count.

Disabled, missing, or invalid authentication fails closed. The Twenty function
uses a ten-second timeout, validates the response against a fixed schema, and
returns a bounded unavailable state without forwarding gateway error bodies.

## Non-goals

- embedding the normal Codex-LB dashboard;
- routing, account, credential, key, or configuration writes from Twenty;
- exposing raw request logs or arbitrary query/filter input;
- making Codex-LB an identity or Workspace authority; or
- enabling a live environment from this source change.
