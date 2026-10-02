"""Add optional operator-maintained billing calendar dates."""

import sqlalchemy as sa
from alembic import op

revision = "20261002_230000_add_account_billing_dates"
down_revision = "20260918_000000_merge_scim_and_overflow_heads"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for name in ("billing_renewal_date", "billing_paid_through_date", "billing_cancel_review_date"):
        op.add_column("accounts", sa.Column(name, sa.Date(), nullable=True))


def downgrade() -> None:
    for name in ("billing_cancel_review_date", "billing_paid_through_date", "billing_renewal_date"):
        op.drop_column("accounts", name)
