"""update userevent

Revision ID: e3fad42bc3f9
Revises: e6fe07dbd2f8
Create Date: 2025-01-24 16:36:52.902743

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e3fad42bc3f9"
down_revision: Union[str, None] = "e6fe07dbd2f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_userevents_event_id_events", "userevents", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_userevents_event_id_events"),
        "userevents",
        "events",
        ["event_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_userevents_event_id_events"), "userevents", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_userevents_event_id_events",
        "userevents",
        "events",
        ["event_id"],
        ["id"],
    )
