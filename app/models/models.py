from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    __table_args__ = {"extend_existing": True}

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)


class Event(Base):
    __table_args__ = {"extend_existing": True}

    chat_id: Mapped[int] = mapped_column(Integer, nullable=True)
    event_name: Mapped[str] = mapped_column(String, nullable=True)


class UserEvent(Base):
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
