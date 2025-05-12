from datetime import datetime

from sqlalchemy import String, Boolean, ForeignKey, BigInteger, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseEvent


class Event(BaseEvent):
    __table_args__ = {"extend_existing": True}

    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    event_name: Mapped[str] = mapped_column(String, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    minimum_participants: Mapped[int] = mapped_column(
        BigInteger, default=10, nullable=True
    )
    event_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )


class UserEvent(BaseEvent):
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE")
    )
    user_choice: Mapped[str] = mapped_column(String, nullable=True)
