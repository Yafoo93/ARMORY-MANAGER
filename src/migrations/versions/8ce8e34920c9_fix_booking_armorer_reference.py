import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8ce8e34920c9"
down_revision = "fe0487239352"
branch_labels = None
depends_on = None


def upgrade():
    # Use batch mode to alter bookings table safely
    with op.batch_alter_table("bookings", schema=None) as batch_op:
        batch_op.add_column(sa.Column("armorer_id", sa.Integer(), nullable=False))
        batch_op.create_foreign_key("fk_bookings_armorer_id_users", "users", ["armorer_id"], ["id"])


def downgrade():
    with op.batch_alter_table("bookings", schema=None) as batch_op:
        batch_op.drop_constraint("fk_bookings_armorer_id_users", type_="foreignkey")
        batch_op.drop_column("armorer_id")
