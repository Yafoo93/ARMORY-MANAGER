"""create weapons table

Revision ID: create_weapons_table
Revises: create_users_table
Create Date: 2024-03-20
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "create_weapons_table"
down_revision: Union[str, None] = "create_users_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "weapons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("serial_no", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("condition", sa.String(), nullable=False),
        sa.Column("last_service", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("serial_no"),
    )


def downgrade() -> None:
    op.drop_table("weapons")
