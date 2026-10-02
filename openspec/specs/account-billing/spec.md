# account-billing Specification

## Purpose
Show operator-maintained subscription dates independently of quota windows.

## Requirements
### Requirement: Manually maintained billing dates
The system SHALL persist optional renewal, paid-through, and cancellation-review calendar dates per account, independently of quota reset windows. Existing accounts SHALL have unknown dates. The API SHALL accept only ISO calendar date strings or null, and require accounts write permission for updates. All three fields SHALL be required on replacement updates. Deleted or deletion-pending accounts SHALL return not found.

#### Scenario: Save and clear dates
- **WHEN** an authorized operator saves valid dates or null values
- **THEN** subsequent account listings show those values without changing routing, credentials, or usage history

#### Scenario: Invalid or unauthorized update
- **WHEN** a request has an invalid date or lacks write permission
- **THEN** the update is rejected and existing data remains unchanged

### Requirement: Informational billing guidance
The account detail SHALL label dates as manually entered and show cancellation review when due, verify-date guidance for past dates, and consider-use-first guidance when a renewal or paid-through date is within seven calendar days and the account is active with known available quota. Suggestions SHALL NOT mutate routing or perform cancellation. Past dates SHALL NOT be automatically advanced or treated as proof of expiry.

#### Scenario: Date arrives
- **WHEN** a saved cancellation-review date is today or earlier
- **THEN** the dashboard suggests reviewing cancellation with the subscription provider

#### Scenario: Approaching renewal
- **WHEN** an active account with available quota has a renewal date within seven days
- **THEN** the dashboard suggests considering use first and explains billing dates do not reset quota

### Requirement: Dashboard billing comparison
The dashboard accounts list SHALL show a Billing column containing saved dates and informational suggestions. Account cards SHALL show the same summary. Empty dates SHALL be labeled as not entered, and the list SHALL support sorting by earliest entered billing date with unknown dates last. Sorting SHALL NOT affect routing.

#### Scenario: Compare accounts
- **WHEN** the operator views dashboard accounts
- **THEN** renewal, paid-through, and cancellation-review dates are visible without opening each account
