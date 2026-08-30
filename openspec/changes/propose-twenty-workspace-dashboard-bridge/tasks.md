## 1. Proposal and authority

- [x] 1.1 Record the native server-to-server path in OpenSpec.
- [x] 1.2 Bind the change to the Mhoo authority split and repository ownership.
- [x] 1.3 Record that source implementation does not authorize live enablement.

## 2. API and security design

- [x] 2.1 Define the versioned endpoint, windows, and response schema.
- [x] 2.2 Define the distinct presence-enabled service identity, startup validation, audit,
  timeout, and rate-limit contracts.
- [x] 2.3 Complete the field-level privacy, retention, and logging boundary.
- [x] 2.4 Reject iframe support from the first implementation.

## 3. Codex-LB implementation

- [x] 3.1 Add API-key Workspace attribution and the disabled aggregate route.
- [x] 3.2 Add authentication, rate limit, audit, validation, and route coverage.
- [x] 3.3 Add the database migration and default-off environment example.

## 4. Cross-repository integration

- [x] 4.1 Implement the owner-gated Twenty App function and native component in
  `mhoo-twenty`.
- [ ] 4.2 Add Infrastructure-owned network, secret, deployment, and recovery
  definitions after architecture acceptance.
- [ ] 4.3 Install the App, bind live keys, and verify exactly one full server
  admin in the target environment.

## 5. Verification

- [x] 5.1 Run focused denied/allowed identity, privacy-boundary, aggregation,
  duplicate-binding, lint, and type checks.
- [x] 5.2 Build and test the Twenty App manifest and server function locally.
- [ ] 5.3 Prove the actual cross-host owner UI without production traffic or
  expanded authority.
- [ ] 5.4 Complete independent review, CI, Mhoo ADR acceptance, and
  Infrastructure enablement gates.
