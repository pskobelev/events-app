from datetime import datetime

from sqlalchemy import String, Boolean, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class Event(Base):
    __table_args__ = {"extend_existing": True}

    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    event_name: Mapped[str] = mapped_column(String, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

class UserEvent(Base):
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    user_choice: Mapped[str] = mapped_column(String, nullable=True)
