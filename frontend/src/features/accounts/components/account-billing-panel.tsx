import { useState } from "react";
import { useTranslation } from "react-i18next";
import { billingGuidance } from "@/features/accounts/billing-guidance";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import type { AccountBilling, AccountSummary } from "@/features/accounts/schemas";

const fields = [
  ["billingRenewalDate", "accounts.billing.renewal"],
  ["billingPaidThroughDate", "accounts.billing.paidThrough"],
  ["billingCancelReviewDate", "accounts.billing.cancelReview"],
] as const;

export function AccountBillingPanel({ account, busy, readOnly, onSave }: {
  account: AccountSummary;
  busy: boolean;
  readOnly: boolean;
  onSave?: (accountId: string, billing: AccountBilling) => Promise<unknown>;
}) {
  const { t } = useTranslation();
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [draft, setDraft] = useState<AccountBilling>({
    billingRenewalDate: account.billingRenewalDate ?? null,
    billingPaidThroughDate: account.billingPaidThroughDate ?? null,
    billingCancelReviewDate: account.billingCancelReviewDate ?? null,
  });
  const { review, stale, useFirst } = billingGuidance(account);
  const disabled = busy || saving || readOnly;

  const save = async () => {
    if (!onSave || disabled) return;
    setSaving(true);
    setError(null);
    try {
      await onSave(account.accountId, draft);
      setEditing(false);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : t("common.errors.unknown"));
    } finally {
      setSaving(false);
    }
  };

  return <section className="space-y-3 rounded-lg border p-3" aria-label={t("accounts.billing.title")}>
    <div className="flex items-center justify-between gap-2">
      <h3 className="text-sm font-medium">{t("accounts.billing.title")}</h3>
      {!editing && !readOnly && onSave ? <Button variant="ghost" size="sm" disabled={disabled} onClick={() => {
        setDraft({ billingRenewalDate: account.billingRenewalDate ?? null, billingPaidThroughDate: account.billingPaidThroughDate ?? null, billingCancelReviewDate: account.billingCancelReviewDate ?? null });
        setError(null);
        setEditing(true);
      }}>{t("accounts.billing.edit")}</Button> : null}
    </div>
    <p className="text-xs text-muted-foreground">{t("accounts.billing.manual")}</p>
    {editing ? <form className="space-y-3" onSubmit={(event) => { event.preventDefault(); void save(); }}>
      {fields.map(([key, label]) => <label key={key} className="block space-y-1 text-xs">
        <span>{t(label)}</span>
        <Input type="date" aria-label={t(label)} value={draft[key] ?? ""} disabled={disabled} min="0001-01-01" max="9999-12-31"
          onChange={(event) => setDraft({ ...draft, [key]: event.target.value || null })} />
      </label>)}
      {error ? <p role="alert" className="text-xs text-destructive">{error}</p> : null}
      <div className="flex gap-2">
        <Button type="submit" size="sm" disabled={disabled}>{t("accounts.billing.save")}</Button>
        <Button type="button" variant="ghost" size="sm" disabled={saving} onClick={() => setEditing(false)}>{t("common.cancel")}</Button>
      </div>
    </form> : <dl className="space-y-2 text-xs">{fields.map(([key, label]) => <div key={key} className="flex justify-between gap-3">
      <dt className="text-muted-foreground">{t(label)}</dt><dd>{account[key] ?? t("accounts.billing.unknown")}</dd>
    </div>)}</dl>}
    {review ? <p className="text-xs font-medium">{t("accounts.billing.review")}</p> : null}
    {stale ? <p className="text-xs font-medium">{t("accounts.billing.stale")}</p> : null}
    {useFirst ? <p className="text-xs font-medium">{t("accounts.billing.useFirst")}</p> : null}
    <p className="text-xs text-muted-foreground">{t("accounts.billing.quotaNote")}</p>
  </section>;
}
