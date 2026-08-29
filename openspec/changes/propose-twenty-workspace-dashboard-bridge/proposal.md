## Why

Mhoo is evaluating Codex-LB as a separately hosted model-routing and
operational-telemetry service while Twenty remains the human, role, Workspace,
and application UI authority. Operators need an explicit contract for showing
Codex-LB insight inside a Twenty Workspace without granting the browser a
Codex-LB admin credential, treating a Workspace ID as authentication, or moving
Codex-LB telemetry into a second business-state authority.

The current repository has no Twenty-specific read API, embed session, or
Workspace dashboard integration. Documenting the proposed boundary before
implementation keeps that absence visible and gives the security and product
design a testable review target.

## What Changes

- Propose a disabled-by-default `twenty-workspace-dashboard-bridge` capability.
- Prefer native rendering in a Twenty front component backed by a Twenty
  server-side function that calls a bounded, read-only Codex-LB telemetry API.
- Keep every Codex-LB credential server-side and require a dedicated
  service-to-service identity; caller-supplied Workspace or user identifiers
  remain context, never authority.
- Define a conditional iframe path only for a dedicated, short-lived,
  read-only embed session with explicit framing and origin controls.
- Preserve the ownership split: Twenty owns people, roles, navigation, and
  Workspace UI; Codex-LB owns only its routing and operational telemetry.
- Add no implementation, deployment, setting, route, credential, or dashboard
  behavior in this documentation change.

## Capabilities

### New Capabilities

- `twenty-workspace-dashboard-bridge`: proposed contracts for a read-only
  native data path and an optional constrained dashboard embed.

### Modified Capabilities

None.

## Impact

This change adds OpenSpec documentation only. It has no runtime, API, schema,
frontend, migration, deployment, credential, or production effect. Future
implementation remains blocked on an API and threat-model review,
repository-owned tests, a Twenty App integration owned by `mhoo-twenty`, and
Infrastructure-owned deployment and recovery approval. Accepted ADR-0008 fixes
the ownership boundary but does not satisfy any of those capability gates.
