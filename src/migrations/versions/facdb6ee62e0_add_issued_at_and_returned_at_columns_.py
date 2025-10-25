import sqlalchemy as sa
from alembic import op

revision = "stepA_add_timestamps"
down_revision = "8ce8e34920c9"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("bookings", schema=None) as batch_op:
        batch_op.add_column(sa.Column("issued_at", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("returned_at", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("ammunition_count", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("ammunition_returned", sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table("bookings", schema=None) as batch_op:
        batch_op.drop_column("ammunition_returned")
        batch_op.drop_column("ammunition_count")
        batch_op.drop_column("returned_at")
        batch_op.drop_column("issued_at")
