## 1. Proposal and authority

- [x] 1.1 Record the proposed native and conditional iframe paths in OpenSpec.
- [x] 1.2 Keep the change documentation-only and make current non-implementation
  explicit.
- [x] 1.3 Bind the change to accepted ADR-0008 architecture and repository
  ownership without treating that decision as feature implementation.

## 2. API and security design

- [ ] 2.1 Define the versioned read-only projection and response schemas.
- [ ] 2.2 Select and threat-model the service-to-service identity, rotation,
  revocation, audit, timeout, and rate-limit contracts.
- [ ] 2.3 Complete field-level privacy, retention, and logging review.
- [ ] 2.4 Decide whether the iframe path is needed; if so, specify the dedicated
  embed session, framing, origin, CSRF, cookie, and messaging contracts.

## 3. Codex-LB implementation

- [ ] 3.1 Implement the bounded telemetry route behind a disabled-by-default
  capability gate.
- [ ] 3.2 Add authentication, scope, error, audit, and secret-redaction coverage.
- [ ] 3.3 If accepted, implement the dedicated read-only embed surface without
  reusing the privileged dashboard session.

## 4. Cross-repository integration

- [ ] 4.1 Implement the Twenty App function and native front component in the
  repository selected by the accepted Mhoo architecture.
- [ ] 4.2 Add Infrastructure-owned TLS, network, secret-delivery, recovery, and
  deployment definitions for an authorized disposable environment.
- [ ] 4.3 Add user documentation only after the behavior is implemented and link
  it to the accepted capability spec.

## 5. Verification

- [ ] 5.1 Prove allowed and denied service identities, scopes, fields, windows,
  origins, sessions, and failure paths.
- [ ] 5.2 Prove that browser state and logs contain no bridge, admin, API-key, or
  account credential.
- [ ] 5.3 Prove the actual cross-host native dashboard and, if selected, iframe
  behavior without production traffic or authority.
- [ ] 5.4 Run strict OpenSpec validation, repository tests, an independent
  security review, and the applicable Mhoo/Infrastructure acceptance gates.
