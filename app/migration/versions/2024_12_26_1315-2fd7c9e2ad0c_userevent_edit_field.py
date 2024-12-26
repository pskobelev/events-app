"""userevent edit field

Revision ID: 2fd7c9e2ad0c
Revises: ad25b41b44b1
Create Date: 2024-12-26 13:15:44.283873

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "2fd7c9e2ad0c"
down_revision: Union[str, None] = "ad25b41b44b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "userevents", "user_id", existing_type=sa.BIGINT(), nullable=True
    )
    op.drop_constraint(
        "fk_userevents_user_id_users", "userevents", type_="foreignkey"
    )


def downgrade() -> None:
    op.create_foreign_key(
        "fk_userevents_user_id_users",
        "userevents",
        "users",
        ["user_id"],
        ["telegram_id"],
    )
    op.alter_column(
        "userevents", "user_id", existing_type=sa.BIGINT(), nullable=False
    )
