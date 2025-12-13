from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseEvent


class User(BaseEvent):
    __table_args__ = {"extend_existing": True}

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
