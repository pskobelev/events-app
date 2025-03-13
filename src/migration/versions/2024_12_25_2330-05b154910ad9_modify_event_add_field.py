"""modify event, add field

Revision ID: 05b154910ad9
Revises: 64c5416060b1
Create Date: 2024-12-25 23:30:16.951780

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "05b154910ad9"
down_revision: Union[str, None] = "64c5416060b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "events", sa.Column("event_date", sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("events", "event_date")
