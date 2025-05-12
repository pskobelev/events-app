from datetime import datetime

from sqlalchemy import DateTime, func, MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    class_mapper,
)

from src.config import settings


class BaseEvent(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

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

    metadata = MetaData(
        naming_convention=settings.db.convention,
    )

    # чтобы не придумывать названия таблиц, они будут создаваться от класса
    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower() + "s"

    def as_dict(self):
        columns = class_mapper(self.__class__).columns
        return {c.name: getattr(self, c.name) for c in columns}
