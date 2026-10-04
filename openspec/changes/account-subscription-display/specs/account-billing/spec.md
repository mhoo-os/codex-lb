## ADDED Requirements
### Requirement: Provider subscription snapshot
Account summaries SHALL expose optional subscription active-start, active-until, and provider-last-checked timestamps from that account's saved ID token. Invalid or absent timestamps SHALL yield unknown values without breaking identity parsing. Reversed start/end ranges SHALL be omitted. These fields SHALL NOT be writable via manual billing updates or inferred from quota resets. No token content other than these timestamps SHALL be added to responses.

#### Scenario: Account-specific dates
- **WHEN** two accounts have different subscription claims
- **THEN** each summary shows only its own subscription dates, preserving manual reminders

#### Scenario: Invalid claim
- **WHEN** a timestamp is malformed, lacks a timezone, or is absent
- **THEN** that timestamp is unknown and account identity remains readable

### Requirement: Honest subscription display
The dashboard table, cards, and account detail SHALL show the provider-reported subscription active period and provider last-checked date when available, labeled as a saved sign-in snapshot in UTC. The UI SHALL explain that these dates do not confirm the next charge or invoice cycle. Missing provider dates SHALL be labeled unavailable, independently of manual reminders. Past active-until dates SHALL be labeled for verification without asserting cancellation. Manual reminder editing and routing SHALL remain unchanged. Billing sorting SHALL include known provider active-until timestamps with unknown values last.

#### Scenario: Existing account without manual reminders
- **WHEN** an account has provider subscription dates but no manually entered dates
- **THEN** its provider dates are visible instead of an isolated Not entered label
