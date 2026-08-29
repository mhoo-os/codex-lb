## Context

See [`proposal.md`](proposal.md) for motivation and [`context.md`](context.md)
for the authority and product background. Codex-LB currently has no
Twenty-specific telemetry API, embed session, or Workspace dashboard. Twenty
and Codex-LB may run on different hosts, and accepted Mhoo ADR-0008 keeps
people, roles, navigation, and Workspace UI in Twenty while Codex-LB owns only
model routing and its operational telemetry.

The implementation must therefore cross a host boundary without placing a
Codex-LB credential in the browser, treating a caller-supplied Workspace value
as authority, or exposing the privileged Codex-LB dashboard. The normative
security and failure requirements are in
[`specs/twenty-workspace-dashboard-bridge/spec.md`](specs/twenty-workspace-dashboard-bridge/spec.md).

## Goals / Non-Goals

**Goals:**

- define an implementation shape for a native, read-only Twenty dashboard;
- keep authentication, data projection, and failure behavior explicit at the
  cross-host boundary;
- preserve a narrowly constrained iframe option only if it earns a separate
  embed security design; and
- allow a future implementation to remain disabled until its API, security,
  Twenty integration, and Infrastructure gates pass.

**Non-Goals:**

- select a production credential, hostname, network provider, or deployment;
- define the final telemetry response schema before task 2.1;
- expose Codex-LB routing, account, API-key, credential, or configuration
  writes; or
- implement a route, session, front component, setting, migration, or live
  effect in this documentation change.

## Decisions

### Prefer native Twenty rendering through a server-side App function

The primary path is:

```text
Twenty front component
  -> Twenty server-side App function
  -> authenticated read-only Codex-LB telemetry API
  -> allow-listed view model
  -> native Twenty cards, charts, and tables
```

The App function acts as a bounded backend-for-frontend. It holds the
service-to-service credential, requests only a named projection, and returns
only the fields required by the Workspace surface. This keeps browser CORS,
third-party cookies, and `Origin` behavior out of the authorization boundary.

A direct browser-to-Codex-LB call is rejected because it would either disclose
a reusable credential or make browser-controlled state part of authentication.
Embedding the existing admin dashboard is also rejected because it would
couple Workspace presentation to a privileged session and write-capable UI.

### Use a fixed read-only projection contract

Codex-LB will expose a versioned endpoint with named, allow-listed projections,
filters, fields, and aggregation windows. The precise path and response schema
remain task 2.1, but the endpoint will not accept SQL, arbitrary field lists,
repository-object selectors, or pass-through admin API input.

Serving bounded aggregates from Codex-LB preserves telemetry ownership and
avoids creating a second canonical copy of routing data inside Twenty. Twenty
owns the rendered Workspace experience, not the underlying Codex-LB telemetry.

### Authenticate the service before applying Workspace context

Codex-LB will authenticate one dedicated server-side service identity and then
apply its fixed read-only scope. A Workspace or user identifier may be carried
for filtering and audit only after that authentication succeeds. It cannot
expand the service identity's scope or select otherwise inaccessible data.

The credential mechanism, rotation, revocation, and audit format remain task
2.2. Reusing an admin cookie, a user browser session, or a general Codex-LB API
key is not an eligible implementation.

### Treat iframe support as a separate conditional surface

If later product review proves that native rendering cannot preserve a needed
experience, Codex-LB may add a dedicated read-only embed surface. It requires
a short-lived scoped session, exact origin and `frame-ancestors` controls,
validated cross-window messages, and no privileged dashboard routes or write
actions. The normal admin dashboard and its session are never embedded.

This option remains disabled unless task 2.4 accepts its threat model. Native
rendering remains the default and does not depend on iframe support.

### Fail closed with a bounded unavailable state

Authentication, scope, timeout, network, projection, and upstream-data errors
return a bounded error to the Twenty App function. The Workspace UI may show an
unavailable or stale indicator, but neither side falls back to direct database
access, a browser credential, a caller-supplied authority selector, or a
write-capable route.

## Risks / Trade-offs

- **[Service credential becomes broadly privileged]** -> Give it a dedicated
  read-only audience and scope, keep it server-side, rotate and revoke it, and
  test denied identities and projections.
- **[An allow-listed aggregate still leaks sensitive telemetry]** -> Review
  every field for source, sensitivity, retention, Workspace visibility, and
  logging before adding it to a projection.
- **[Cross-host latency or outage degrades the Workspace]** -> Bound timeouts,
  return an explicit unavailable/stale view model, and keep the rest of the
  Workspace usable.
- **[Workspace context is mistaken for authorization]** -> Authenticate and
  scope the service first; treat context only as a validated filter and audit
  attribute.
- **[Iframe support recreates a privileged dashboard path]** -> Keep it
  optional, use a separate read-only surface and session, and reject the option
  if its threat model cannot pass.
- **[Native rendering duplicates some dashboard presentation work]** -> Accept
  that cost to preserve Twenty-native roles, navigation, and browser security;
  share only the bounded data contract, not an admin session.

## Migration Plan

There is no existing bridge or data to migrate. A future implementation must:

1. complete and approve the response schema and service-identity threat model;
2. implement the disabled Codex-LB read route and denial coverage;
3. implement the Twenty App function and native component in `mhoo-twenty`;
4. provision an authorized isolated network route and secret-delivery path
   through Infrastructure;
5. prove allowed, denied, unavailable, stale, and secret-redaction behavior
   across the real hosts; and
6. obtain separate approval before enabling any non-disposable environment.

Rollback is disabling the capability and removing its service credential and
route while leaving Twenty and Codex-LB operating independently. Production
traffic, deployment, and credential mutation are outside this change.

## Open Questions

- Which first projection and aggregation windows provide useful operator
  insight without exposing request-level private data?
- Which dedicated service-identity mechanism best fits the accepted network
  and rotation controls?
- Does any required visual interaction justify the conditional iframe surface,
  or can native Twenty rendering cover the complete first use case?
