import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AccountBillingPanel } from "./account-billing-panel";
import { createAccountSummary } from "@/test/mocks/factories";

afterEach(() => vi.useRealTimers());

describe("AccountBillingPanel", () => {
  it("saves calendar dates and clears empty fields", async () => {
    const onSave = vi.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();
    const account = createAccountSummary({ billingRenewalDate: "2026-10-31" });
    render(<AccountBillingPanel account={account} busy={false} readOnly={false} onSave={onSave} />);
    await user.click(screen.getByText("Edit billing dates"));
    fireEvent.change(screen.getByLabelText("Next renewal"), { target: { value: "" } });
    fireEvent.change(screen.getByLabelText("Review cancellation on"), { target: { value: "2026-10-28" } });
    await user.click(screen.getByText("Save dates"));
    expect(onSave).toHaveBeenCalledWith(account.accountId, { billingRenewalDate: null, billingPaidThroughDate: null, billingCancelReviewDate: "2026-10-28" });
  });

  it("shows reminders without invoking a mutation", () => {
    vi.useFakeTimers(); vi.setSystemTime(new Date(2026, 9, 2, 12));
    const onSave = vi.fn();
    render(<AccountBillingPanel account={createAccountSummary({ billingRenewalDate: "2026-10-05", billingCancelReviewDate: "2026-10-02", status: "active", usage: { primaryRemainingPercent: 50, secondaryRemainingPercent: 30 } })} busy={false} readOnly={false} onSave={onSave} />);
    expect(screen.getByText(/Consider using this account first/)).toBeInTheDocument();
    expect(screen.getByText(/Review cancellation with your subscription provider/)).toBeInTheDocument();
    expect(onSave).not.toHaveBeenCalled();
  });

  it.each(["paused", "reauth_required", "quota_exceeded"] as const)("does not suggest using a %s account", (status) => {
    vi.useFakeTimers(); vi.setSystemTime(new Date(2026, 9, 2, 12));
    render(<AccountBillingPanel account={createAccountSummary({ status, billingRenewalDate: "2026-10-05" })} busy={false} readOnly />);
    expect(screen.queryByText(/Consider using this account first/)).not.toBeInTheDocument();
    expect(screen.queryByText("Edit billing dates")).not.toBeInTheDocument();
  });

  it("marks past billing dates for verification without claiming expiry", () => {
    vi.useFakeTimers(); vi.setSystemTime(new Date(2026, 9, 2, 12));
    render(<AccountBillingPanel account={createAccountSummary({ billingRenewalDate: "2026-09-30" })} busy={false} readOnly />);
    expect(screen.getByText(/expiry is not confirmed/)).toBeInTheDocument();
    expect(screen.queryByText(/Consider using this account first/)).not.toBeInTheDocument();
  });

  it("keeps the draft on a save failure", async () => {
    const user = userEvent.setup();
    render(<AccountBillingPanel account={createAccountSummary()} busy={false} readOnly={false} onSave={vi.fn().mockRejectedValue(new Error("Save failed"))} />);
    await user.click(screen.getByText("Edit billing dates"));
    await user.click(screen.getByText("Save dates"));
    expect(screen.getByRole("alert")).toHaveTextContent("Save failed");
    expect(screen.getByLabelText("Next renewal")).toBeInTheDocument();
  });
});
