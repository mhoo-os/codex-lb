import { subscriptionSnapshotIsPast } from "@/features/accounts/billing-guidance";
import { useTranslation } from "react-i18next";
import type { AccountSummary } from "@/features/accounts/schemas";

// Provider timestamps are shown in UTC consistently with their date labels.
function utcDate(value: string | null | undefined) {
  return value ? new Date(value).toISOString().slice(0, 10) : null;
}

export function AccountSubscriptionPeriod({ account, compact = false }: {
  account: AccountSummary;
  compact?: boolean;
}) {
  const { t } = useTranslation();
  const snapshot = account.subscription;
  const start = utcDate(snapshot?.activeStart);
  const until = utcDate(snapshot?.activeUntil);
  const checked = utcDate(snapshot?.lastChecked);
  const past = subscriptionSnapshotIsPast(account);
  return <div className="space-y-1 text-xs" title={t("accounts.billing.providerNote")}>
    <p className="font-medium">{t("accounts.billing.providerTitle")}</p>
    {start || until ? <>
      <p className="tabular-nums">{start ?? t("accounts.billing.unavailable")} → {until ?? t("accounts.billing.unavailable")} (UTC)</p>
      <p className="text-muted-foreground">{t("accounts.billing.providerChecked")}: {checked ? `${checked} (UTC)` : t("accounts.billing.unavailable")}</p>
      {past ? <p className="font-medium">{t("accounts.billing.providerPast")}</p> : null}
    </> : <p className="text-muted-foreground">{t("accounts.billing.providerMissing")}</p>}
    {!compact ? <p className="text-muted-foreground">{t("accounts.billing.providerNote")}</p> : null}
  </div>;
}
