"""upgrade event date

Revision ID: e6fe07dbd2f8
Revises: 1732e6abc711
Create Date: 2025-01-17 11:50:09.739918

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "e6fe07dbd2f8"
down_revision: Union[str, None] = "1732e6abc711"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "events",
        "event_date",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "events",
        "event_date",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
    )
