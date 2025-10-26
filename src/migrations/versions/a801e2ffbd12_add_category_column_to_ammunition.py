import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "a801e2ffbd12"
down_revision = "stepA_add_timestamps"
branch_labels = None
depends_on = None


def upgrade():
    # Check if 'category' column exists before adding (SQLite-safe)
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col["name"] for col in inspector.get_columns("ammunitions")]
    if "category" not in columns:
        op.add_column("ammunitions", sa.Column("category", sa.String(length=50), nullable=True))

    # Drop old unused columns if they exist
    for col in [
        "returned_ammunition_count",
        "date_issued",
        "date_returned",
        "issued_ammunition_count",
    ]:
        col_names = [c["name"] for c in inspector.get_columns("bookings")]
        if col in col_names:
            op.drop_column("bookings", col)
