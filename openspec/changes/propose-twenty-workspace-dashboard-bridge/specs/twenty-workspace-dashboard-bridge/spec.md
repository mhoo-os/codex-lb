# twenty-workspace-dashboard-bridge Delta

## ADDED Requirements

### Requirement: The bridge is disabled by default

Codex-LB MUST NOT serve the Twenty usage response unless
`CODEX_LB_TWENTY_USAGE_BRIDGE_TOKEN` contains at least 32 characters. The
absence of that token MUST be the default-off gate.

#### Scenario: Disabled bridge fails closed

- **GIVEN** no bridge token is configured
- **WHEN** any caller requests the bridge route
- **THEN** Codex-LB returns no telemetry
- **AND** normal proxy behavior is unchanged

### Requirement: Workspace attribution is explicit and unique

An API key MAY carry one normalized `twenty_workspace_id` and
`twenty_workspace_name`. A non-null Workspace ID MUST be unique across API
keys. The mapping MUST be used only to attribute telemetry and MUST NOT grant
authentication or authorization.

#### Scenario: Duplicate Workspace binding is rejected

- **GIVEN** one API key is already bound to a Twenty Workspace ID
- **WHEN** another key is created or updated with the same ID
- **THEN** the operation is rejected
- **AND** the existing binding remains unchanged

#### Scenario: Unbound key is excluded

- **GIVEN** usage exists for an API key with no Twenty Workspace binding
- **WHEN** the bridge aggregates a window
- **THEN** that usage is absent from the response

### Requirement: The API has a fixed read-only response contract

Codex-LB SHALL expose
`GET /api/integrations/twenty/v1/workspace-usage` with only `1d`, `7d`, and
`30d` aggregation windows. It MUST return global and per-bound-Workspace
request, input-token, output-token, cached-input-token, non-success, and
persisted-cost totals plus active/last-used state and per-model aggregates. It
MUST return no more than 100 model aggregates per Workspace, MUST exclude
warm-up request kinds, and MUST perform no mutation.

#### Scenario: Allowed window returns aggregates

- **GIVEN** a valid bridge identity and explicitly bound keys
- **WHEN** the caller requests an allowed window
- **THEN** the route returns the fixed aggregate response
- **AND** totals equal the sum of returned Workspace rows

#### Scenario: Unknown window is rejected

- **WHEN** a caller requests a window outside `1d`, `7d`, or `30d`
- **THEN** Codex-LB rejects the request
- **AND** does not dynamically forward or interpret the value

### Requirement: The response excludes private and credential data

The bridge response MUST NOT include API-key IDs or prefixes, credentials,
account identities, request identifiers, client IPs, bodies, prompts, outputs,
conversation identifiers, error messages, or arbitrary repository fields.

#### Scenario: Aggregate response is privacy bounded

- **WHEN** a valid bridge read succeeds
- **THEN** the response contains only the documented view model
- **AND** browser-visible data contains no reusable Codex-LB credential

### Requirement: Authentication is a dedicated server identity

The route MUST authenticate a distinct bearer token using constant-time
comparison before reading telemetry. Proxy API keys, dashboard sessions,
browser cookies, Workspace IDs, user IDs, hosts, and origins MUST NOT
authenticate the route. A valid identity MUST be rate-limited to 120 reads per
60 seconds.

#### Scenario: Missing or invalid identity is denied

- **WHEN** the bearer token is missing or invalid
- **THEN** Codex-LB returns no telemetry
- **AND** no caller-supplied identifier changes that result

### Requirement: Reads are auditable without secret leakage

Every successful bridge read MUST emit a `twenty_usage_bridge_read` audit event
with the selected window and returned Workspace count. The event and ordinary
logs MUST NOT record the bridge token, proxy key secret, or response payload.

#### Scenario: Successful read is recorded

- **WHEN** a valid bridge request returns aggregate usage
- **THEN** an audit event records non-secret correlation fields
- **AND** no credential is logged

### Requirement: Iframe embedding is not part of this capability

Codex-LB MUST NOT expose the normal dashboard or its session through an iframe
for this capability. Any future embed surface requires a separate accepted
security contract.

#### Scenario: Native path does not require framing

- **WHEN** the Twenty usage UI is used
- **THEN** it receives data through the server-side App route
- **AND** no Codex-LB dashboard page is framed
