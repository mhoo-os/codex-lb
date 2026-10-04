import { format } from "date-fns";
import type { AccountSummary } from "@/features/accounts/schemas";

export function billingGuidance(account: AccountSummary, now = new Date()) {
  const today = format(now, "yyyy-MM-dd");
  const soonDate = new Date(now);
  soonDate.setDate(soonDate.getDate() + 7);
  const soon = format(soonDate, "yyyy-MM-dd");
  const periodDates = [account.billingRenewalDate, account.billingPaidThroughDate].filter((date): date is string => !!date);
  const stale = periodDates.some((date) => date < today);
  const remaining = [account.usage?.primaryRemainingPercent, account.usage?.secondaryRemainingPercent, account.usage?.monthlyRemainingPercent]
    .filter((value): value is number => value != null);
  const useFirst = !stale && account.status === "active" && remaining.length > 0 && remaining.every((value) => value > 0)
    && periodDates.some((date) => date >= today && date <= soon);
  const review = !!account.billingCancelReviewDate && account.billingCancelReviewDate <= today;
  return { review, stale, useFirst };
}

export function subscriptionSnapshotIsPast(account: AccountSummary, now = new Date()) {
  const until = account.subscription?.activeUntil;
  return !!until && new Date(until).getTime() < now.getTime();
}
