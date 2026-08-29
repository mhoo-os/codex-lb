# Twenty Workspace dashboard bridge context

## Purpose and scope

This change explores how a Codex-LB dashboard can appear inside a Mhoo Twenty
Workspace when the frontend and backend live on different hosts. It governs
only the future Codex-LB side of that integration. Mhoo-wide architecture is
governed by accepted [ADR-0008](https://github.com/mhoo-os/mhoo/blob/0e94e6b00a3033215e4df3ab197e5559652c2436/ADR/0008-twenty-framework-platform.md), and the explorable cross-system view lives in
the [Mhoo Archify atlas](https://github.com/mhoo-os/mhoo/blob/0e94e6b00a3033215e4df3ab197e5559652c2436/docs/architecture/archify/codex-lb-workspace-dashboard.html).

ADR-0008 accepts the ownership boundary, but Codex-LB does not currently
implement a Twenty read API, embed gateway, SSO exchange, or Workspace-specific
dashboard. This active change records a candidate capability contract and
deliberately does not add user-facing docs under `docs/`, because there is no
behavior for users to rely on yet.

Normative future requirements are in
[`specs/twenty-workspace-dashboard-bridge/spec.md`](specs/twenty-workspace-dashboard-bridge/spec.md).

## Authority split

Twenty remains authoritative for people, authentication, sessions,
memberships, roles, active Workspace selection, navigation, and the Workspace
UI. Codex-LB remains authoritative only for its model-routing configuration and
operational telemetry. Neither system gains the other's authority merely
because one renders data from the other.

A hostname, iframe origin, Workspace slug, Workspace ID, user ID, request body,
or query parameter is not authentication. A future Codex-LB bridge accepts a
request only from a dedicated server-side service identity. Any Workspace or
user context carried with that request is an auditable filter input after the
service caller is authenticated; it does not grant access by itself.

## Preferred path: native Twenty rendering

The preferred design keeps the user experience native to Twenty:

```text
authorized Workspace user
  -> Twenty page layout / front component
  -> Twenty server-side App function (BFF)
  -> authenticated HTTPS read request
  -> bounded Codex-LB telemetry API
  -> allow-listed dashboard view model
  -> native Twenty charts, status cards, and tables
```

The browser receives no Codex-LB secret. The Twenty function owns the
service-to-service credential and returns only the fields required by the
Workspace surface. Codex-LB does not expose its database, internal repository
objects, admin session, or general proxy-management API through this path.

This design works across hosts because the secret-bearing request is
server-to-server. Browser CORS and third-party-cookie behavior do not become
the authorization boundary. Network policy, TLS, credential delivery,
rotation, telemetry, and recovery remain Infrastructure-owned concerns.

## Conditional path: constrained iframe

An iframe may preserve the existing Codex-LB visual dashboard, but it is a
separate security product rather than a shortcut. It remains disabled unless
the implementation proves:

- a dedicated read-only embed surface, not the normal admin dashboard;
- a short-lived, narrowly scoped session obtained without putting a long-lived
  API key, admin cookie, or bearer token in a URL;
- an exact `frame-ancestors` and allowed-origin policy for the intended Twenty
  host;
- CSRF, clickjacking, referrer, cookie, and `postMessage` behavior for the
  actual same-site or cross-site deployment; and
- explicit logout, expiry, revocation, audit, and failure behavior.

`SameSite=Lax`, a successful manual iframe load, or a wildcard framing policy
is not proof. If these conditions cannot be met, the native read API remains
the only permitted path.

## Data contract and privacy

The first candidate surface is read-only operational insight: aggregate
availability, request volume, latency, token/cost totals, model mix, capacity,
and bounded incident indicators. Raw upstream authorization, account session
material, API-key secrets, request bodies, prompts, model output, and private
operator credentials are out of scope.

The response model must be explicit and allow-listed. Adding a field requires
review of its source, sensitivity, retention, and Workspace presentation. A
generic SQL endpoint, arbitrary query language, raw request-log export, or
browser relay to Codex-LB is not part of this bridge.

## Failure modes

- If service authentication fails, Codex-LB rejects the request without
  falling back to a caller-supplied identifier.
- If Codex-LB is unavailable or times out, the Twenty surface shows bounded
  unavailable or stale-state UI; it does not gain write authority or silently
  query the Codex-LB database.
- If a requested field or filter is outside the allow-list, the API rejects it
  rather than forwarding it dynamically.
- If framing, origin, cookie, or session checks fail, the embed fails closed
  and the native data path remains the fallback design.
- If the API/security design, Twenty integration, deployment, or credential
  custody contract is not accepted and verified, the capability stays disabled
  and unimplemented.

## Concrete example

An authorized Mhoo operator opens a `Model Operations` tab in Twenty. A native
front component asks its App function for the last 24 hours of aggregate
health. The function authenticates to Codex-LB with its server-side service
identity and requests the fixed `overview` projection. Codex-LB returns totals
and status buckets only. Twenty renders the cards and charts under its own role
and navigation controls. The operator cannot use that surface to reveal
Codex-LB credentials, change routing, or write Workspace business records.

## Non-goals

- implementing or deploying either path;
- embedding the privileged Codex-LB admin dashboard;
- granting routing or account-management writes from Twenty;
- making Codex-LB a Workspace, identity, domain-data, or reasoning authority;
- copying Codex-LB telemetry into a new canonical business database;
- selecting a credential format, network provider, hostname, or production
  topology in this repository; or
- treating this proposal as evidence that the bridge, a Mhoo App, or a fresh
  VPS replacement is implemented, deployed, or ready.
