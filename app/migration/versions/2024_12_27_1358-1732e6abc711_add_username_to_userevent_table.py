"""add username to userevent table

Revision ID: 1732e6abc711
Revises: 2fd7c9e2ad0c
Create Date: 2024-12-27 13:58:48.551575

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1732e6abc711"
down_revision: Union[str, None] = "2fd7c9e2ad0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "userevents", sa.Column("username", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("userevents", "username")
