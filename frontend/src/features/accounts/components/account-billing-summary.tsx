import { useTranslation } from "react-i18next";
import { billingGuidance } from "@/features/accounts/billing-guidance";
import type { AccountSummary } from "@/features/accounts/schemas";

export function AccountBillingSummary({ account }: { account: AccountSummary }) {
  const { t } = useTranslation();
  const { review, stale, useFirst } = billingGuidance(account);
  const dates = [
    ["accounts.billing.renewal", account.billingRenewalDate],
    ["accounts.billing.paidThrough", account.billingPaidThroughDate],
    ["accounts.billing.cancelReview", account.billingCancelReviewDate],
  ] as const;
  return <div className="space-y-1 text-xs" title={t("accounts.billing.manual")}>
    {dates.some(([, date]) => date) ? dates.map(([label, date]) => date ? <p key={label}>
      <span className="text-muted-foreground">{t(label)}: </span><span className="tabular-nums">{date}</span>
    </p> : null) : <p className="text-muted-foreground">{t("accounts.billing.unknown")}</p>}
    {review ? <p className="font-medium text-amber-600 dark:text-amber-400" title={t("accounts.billing.review")}>{t("accounts.billing.reviewShort")}</p> : null}
    {stale ? <p className="font-medium" title={t("accounts.billing.stale")}>{t("accounts.billing.staleShort")}</p> : null}
    {useFirst ? <p className="font-medium text-primary" title={t("accounts.billing.quotaNote")}>{t("accounts.billing.useFirstShort")}</p> : null}
  </div>;
}
