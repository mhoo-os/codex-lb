import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AccountBillingPanel } from "./account-billing-panel";
import { AccountBillingSummary } from "./account-billing-summary";
import { createAccountSummary } from "@/test/mocks/factories";

const subscription = { activeStart: "2026-09-24T20:32:25Z", activeUntil: "2026-10-24T20:32:25Z", lastChecked: "2026-09-24T20:34:43Z" };
afterEach(() => vi.useRealTimers());

describe("provider subscription dates", () => {
  it("shows provider dates separately from editable manual reminders", () => {
    render(<AccountBillingPanel account={createAccountSummary({ subscription, billingRenewalDate: "2026-11-01" })} busy={false} readOnly />);
    expect(screen.getByText("2026-09-24 → 2026-10-24 (UTC)")).toBeInTheDocument();
    expect(screen.getByText("Provider last checked: 2026-09-24 (UTC)")).toBeInTheDocument();
    expect(screen.getByText("2026-11-01")).toBeInTheDocument();
    expect(screen.getByText(/not a confirmed invoice cycle/)).toBeInTheDocument();
  });
  it("shows the provider period in dashboard summaries without manual dates", () => {
    render(<AccountBillingSummary account={createAccountSummary({ subscription })} />);
    expect(screen.getByText("2026-09-24 → 2026-10-24 (UTC)")).toBeInTheDocument();
    expect(screen.queryByText("Not entered")).not.toBeInTheDocument();
  });
  it("labels missing provider information distinctly", () => {
    render(<AccountBillingSummary account={createAccountSummary()} />);
    expect(screen.getByText("Subscription dates unavailable")).toBeInTheDocument();
  });
  it("marks a past snapshot for verification without inventing a new period", () => {
    vi.useFakeTimers(); vi.setSystemTime(new Date("2026-11-01T00:00:00Z"));
    render(<AccountBillingSummary account={createAccountSummary({ subscription })} />);
    expect(screen.getByText("Past reported end date — verify with provider")).toBeInTheDocument();
    expect(screen.getByText("2026-09-24 → 2026-10-24 (UTC)")).toBeInTheDocument();
  });
});
