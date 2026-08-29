# twenty-workspace-dashboard-bridge Delta

## ADDED Requirements

### Requirement: The bridge is disabled until its governing contracts are accepted

The Twenty Workspace dashboard bridge MUST be disabled by default and MUST NOT
be presented as implemented or supported until the applicable Mhoo architecture
decision, Codex-LB API and security design, Twenty App integration, and
Infrastructure deployment boundary are each accepted and verified.

#### Scenario: Documentation exists without implementation authority

- **GIVEN** this OpenSpec change exists but one or more governing contracts are
  unaccepted or unverified
- **WHEN** Codex-LB starts
- **THEN** it exposes no Twenty-specific telemetry route or embed session
- **AND** the dashboard presents no Twenty integration setting

### Requirement: Native integration uses a bounded read-only telemetry API

Codex-LB SHALL expose only an explicit, versioned, read-only response contract
for a future native Twenty dashboard. The contract MUST allow-list projections,
filters, response fields, and aggregation windows. It MUST NOT expose arbitrary
database queries, raw internal repository objects, proxy-management writes,
account session material, API-key secrets, request bodies, prompts, or model
output.

#### Scenario: An approved overview projection is returned

- **GIVEN** an authenticated bridge caller requests an allow-listed overview
  projection and aggregation window
- **WHEN** Codex-LB processes the request
- **THEN** it returns only the documented aggregate fields for that projection
- **AND** performs no routing, account, credential, or Workspace mutation

#### Scenario: An unapproved field or query is rejected

- **WHEN** a bridge caller requests an unknown projection, raw query, or field
  outside the allow-list
- **THEN** Codex-LB rejects the request
- **AND** does not dynamically forward the input to its database or admin APIs

### Requirement: Bridge authentication is server-to-server and fail-closed

The native telemetry API MUST authenticate a dedicated server-side service
identity before evaluating any requested data scope. Browser-provided cookies,
hostnames, origins, Workspace slugs, Workspace IDs, user IDs, request bodies,
or query parameters MUST NOT authenticate or authorize the request. Any
Workspace or user context MUST be treated only as an auditable filter after the
service identity is authenticated.

#### Scenario: Authenticated service identity carries bounded context

- **GIVEN** the configured Twenty App server identity is valid
- **WHEN** it requests an allow-listed projection with Workspace context
- **THEN** Codex-LB evaluates the projection under the service identity's fixed
  read-only scope
- **AND** records the supplied context for bounded filtering and audit without
  treating it as authority

#### Scenario: Caller-supplied Workspace ID cannot grant access

- **GIVEN** a request has no valid bridge service identity
- **WHEN** it supplies a known Workspace ID, user ID, origin, or host
- **THEN** Codex-LB rejects the request
- **AND** returns no telemetry

### Requirement: Browser clients never receive a Codex-LB bridge credential

The native path MUST keep its Codex-LB service credential in the Twenty
server-side function. The front component MUST receive only the bounded view
model required for rendering and MUST NOT receive or relay a Codex-LB bearer
token, API-key secret, admin cookie, or reusable service credential.

#### Scenario: Native dashboard renders aggregate data

- **WHEN** an authorized Twenty front component requests dashboard data through
  its server-side function
- **THEN** the browser receives the allow-listed aggregate response
- **AND** browser storage, URLs, logs, and component state contain no Codex-LB
  bridge credential

### Requirement: An iframe uses a dedicated constrained embed session

If Codex-LB implements iframe embedding, it MUST use a dedicated read-only
embed surface and a short-lived, narrowly scoped embed session. It MUST NOT
reuse the normal admin dashboard session, expose a long-lived credential in a
URL, or enable routing, account, API-key, credential, or configuration writes.
The response MUST apply an exact allowed-origin and `frame-ancestors` policy,
and any cross-window messaging MUST validate the exact peer origin and message
schema.

#### Scenario: Approved host opens a read-only embed

- **GIVEN** a valid short-lived embed session scoped to the approved Twenty
  host and read-only dashboard surface
- **WHEN** that host frames the embed URL
- **THEN** Codex-LB renders only the scoped surface
- **AND** rejects privileged dashboard routes and write actions

#### Scenario: Unapproved framing fails closed

- **WHEN** an unapproved origin frames the embed, the session is expired, or a
  message has an unexpected origin or schema
- **THEN** Codex-LB reveals no dashboard data
- **AND** performs no state change

### Requirement: Cross-host failure does not transfer authority

Timeout, network, authentication, scope, and upstream-data failures MUST return
a bounded error without falling back to direct database access, browser-held
admin credentials, a caller-supplied Workspace selector, or a write-capable
route. The failure MUST be observable without logging secrets or raw private
payloads.

#### Scenario: Codex-LB is unavailable

- **WHEN** the Twenty-side caller cannot reach Codex-LB within the governed
  timeout
- **THEN** the request fails with a bounded unavailable result
- **AND** no alternative authority or write path is attempted
- **AND** the failure can be correlated using non-secret request metadata
