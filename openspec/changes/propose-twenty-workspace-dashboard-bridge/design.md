## Context

Codex-LB and Twenty run as separate services. A browser-to-Codex-LB call would
either disclose a reusable credential or make browser-controlled state part of
authorization. A native Twenty App backend-for-frontend preserves the existing
authority split and avoids a paid Twenty audit/usage dependency.

## Decisions

### Use a fixed aggregate endpoint

The bridge exposes only:

`GET /api/integrations/twenty/v1/workspace-usage?window=1d|7d|30d`

The response carries `generatedAt`, `window`, `windowStartedAt`, global totals,
and one row per explicitly bound Workspace. Each row carries Workspace ID/name,
key active/last-used status, aggregate counters, cost, and up to 100 per-model
aggregates for each Workspace. There is no projection name or arbitrary fields
parameter.

### Bind a Workspace to its dedicated proxy key

`api_keys.twenty_workspace_id` is nullable and unique;
`api_keys.twenty_workspace_name` is nullable display context. Existing keys are
unchanged until explicitly bound. This reuses the key already responsible for
request attribution instead of introducing a second telemetry ownership box.

### Use a distinct off-by-default service credential

The bridge does not reuse proxy keys or dashboard sessions. Operators must
provision one separate bearer token; its absence is the default-off gate. This
avoids adding a second feature toggle to the configuration surface. The token
is compared in constant time and the fixed identity is database rate-limited
after successful authentication.

### Keep the browser behind the Twenty App function

The front component calls only its authenticated `/s/codex-lb/usage` App
route. The function re-queries `currentUser.canAccessFullAdminPanel`, reads
server-only bridge variables, calls Codex-LB, validates the allow-listed
response, and returns it. UI visibility is a convenience, not the security
boundary.

### Do not implement iframe support

The first surface is native and covers the required cards and Workspace table.
No embed session, framing policy, cookie exception, or privileged dashboard
reuse is introduced. Iframe support would require a separate proposal.

## Rollout and rollback

Source may merge while the bridge token remains absent. Live enablement requires
the governing Mhoo ADR to be accepted, both repositories to pass review, the
App to be installed in the intended Workspace, exactly one full server admin
to be verified for the owner-only policy, the service secret to be provisioned,
and each intended proxy key to be bound to its immutable Workspace ID.

Rollback removes and revokes the bridge token. Twenty and
normal Codex-LB proxy traffic continue independently.
