"""add optional Twenty Workspace attribution to API keys

Revision ID: 20260830_000000_add_twenty_workspace_api_key_binding
Revises: 20260806_120000_add_http_bridge_owner_process_epoch
Create Date: 2026-08-30 00:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.engine import Connection

revision = "20260830_000000_add_twenty_workspace_api_key_binding"
down_revision = "20260806_120000_add_http_bridge_owner_process_epoch"
branch_labels = None
depends_on = None

_TABLE = "api_keys"
_ID_COLUMN = "twenty_workspace_id"
_NAME_COLUMN = "twenty_workspace_name"
_CONSTRAINT = "uq_api_keys_twenty_workspace_id"


def _columns(connection: Connection) -> set[str]:
    inspector = sa.inspect(connection)
    if not inspector.has_table(_TABLE):
        return set()
    return {str(column["name"]) for column in inspector.get_columns(_TABLE) if column.get("name") is not None}


def _unique_constraints(connection: Connection) -> set[str]:
    inspector = sa.inspect(connection)
    if not inspector.has_table(_TABLE):
        return set()
    return {
        str(constraint["name"])
        for constraint in inspector.get_unique_constraints(_TABLE)
        if constraint.get("name") is not None
    }


def upgrade() -> None:
    bind = op.get_bind()
    columns = _columns(bind)
    with op.batch_alter_table(_TABLE) as batch_op:
        if _ID_COLUMN not in columns:
            batch_op.add_column(sa.Column(_ID_COLUMN, sa.String(length=128), nullable=True))
        if _NAME_COLUMN not in columns:
            batch_op.add_column(sa.Column(_NAME_COLUMN, sa.String(length=128), nullable=True))

    if _CONSTRAINT not in _unique_constraints(bind):
        with op.batch_alter_table(_TABLE) as batch_op:
            batch_op.create_unique_constraint(_CONSTRAINT, [_ID_COLUMN])


def downgrade() -> None:
    bind = op.get_bind()
    if _CONSTRAINT in _unique_constraints(bind):
        with op.batch_alter_table(_TABLE) as batch_op:
            batch_op.drop_constraint(_CONSTRAINT, type_="unique")

    columns = _columns(bind)
    with op.batch_alter_table(_TABLE) as batch_op:
        if _NAME_COLUMN in columns:
            batch_op.drop_column(_NAME_COLUMN)
        if _ID_COLUMN in columns:
            batch_op.drop_column(_ID_COLUMN)
