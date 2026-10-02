# Account billing dates

Specification: [account-billing](../openspec/specs/account-billing/spec.md).

The dashboard Accounts table includes a **Billing** column; card view shows the same dates and suggestions. Sort Billing to compare the earliest entered dates (unknown dates appear last). Sorting only changes display order.

Open an account and select **Edit billing dates**. Enter the next renewal, paid-through date, or a date to review cancellation. Leave a field blank to clear it. These calendar dates are maintained manually; verify them with the subscription provider. Existing accounts start with unknown dates.

The panel suggests reviewing cancellation when the review date is due. It suggests considering use first when a billing date is within seven days and the active account has known available quota. Use the existing routing-policy control if you decide to change priority. Dates and suggestions never change routing or cancel a subscription.

Billing dates are separate from quota resets. Past billing dates prompt verification; they do not prove expiry or advance automatically. Reminders appear in the dashboard only, with no background notifications.
