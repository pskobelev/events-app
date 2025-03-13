"""upgrade event date, add minumim participants

Revision ID: 9687879e8877
Revises: e3fad42bc3f9
Create Date: 2025-02-28 13:40:33.147157

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "9687879e8877"
down_revision: Union[str, None] = "e3fad42bc3f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "events",
        sa.Column("minimum_participants", sa.BigInteger(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("events", "minimum_participants")
