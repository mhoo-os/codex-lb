## Why
Billing shows Not entered even though saved account sign-in data contains provider-reported subscription dates.

## What Changes
Expose subscription active start, active until, and provider last-checked timestamps from each account's saved ID token. Show this read-only snapshot in account details, dashboard tables and cards. Preserve manual renewal/cancellation reminders separately. Do not claim these timestamps establish an invoice cycle or automatic renewal.

## Impact
Additive account summary fields and dashboard rendering only; no database migration, upstream requests, routing changes, or credential changes.
