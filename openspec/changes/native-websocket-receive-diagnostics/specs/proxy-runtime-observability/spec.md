## ADDED Requirements

### Requirement: Native WebSocket receive diagnostics are bounded and private
The native WebSocket adapter MUST log receive failures using an allowlisted failure phase, mapping unknown phases to `other` and non-transport native errors to `protocol`. Native close frames MUST log only a numeric code in the range 1000 through 4999, or no code when absent or invalid. Logs MUST omit raw exception text, close reasons, headers, payloads, account identity, and call identifiers. The diagnostics MUST NOT change relay messages, error classification, cancellation propagation, account selection, or retry behavior.

#### Scenario: Receive transport fails
- **WHEN** the native adapter receives a transport exception
- **THEN** it emits a bounded failure-phase diagnostic
- **AND** returns the existing relay error unchanged

#### Scenario: Untrusted diagnostic text
- **WHEN** an exception phase, message, or close reason contains arbitrary text
- **THEN** only the allowlisted category and validated numeric close code can appear in the diagnostic

#### Scenario: Cancellation and data
- **WHEN** receive is cancelled or a normal data frame arrives
- **THEN** the adapter emits no failure or close diagnostic
- **AND** preserves cancellation or data delivery
