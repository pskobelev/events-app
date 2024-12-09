from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, \
    declared_attr, class_mapper


class Base(AsyncAttrs, DeclarativeBase):
    """
    An abstract base class for SQLAlchemy models with asynchronous attributes.

    Attributes:
        id (Mapped[int]): The primary key for the model.
        created_at (Mapped[DateTime]): The timestamp when the record was created,
            with a default value of the current timestamp.
        updated_at (Mapped[DateTime]): The timestamp when the record was last updated,
            automatically set to the current timestamp on update.
    """

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

    # чтобы не придумывать названия таблиц, они будут создаваться от класса
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    def as_dict(self):
        columns = class_mapper(self.__class__).columns
        return {c.name: getattr(self, c.name) for c in columns}
