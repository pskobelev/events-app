from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models."""

    __abstract__ = True

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        server_default=func.current_timestamp(),
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
    )
