from sqlalchemy import ForeignKey, Integer, String, BigInteger, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

user_event_association = Table(
    "user_event",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    events = relationship(
        "Event",
        secondary=user_event_association,
        back_populates="users",
    )


class Event(Base):
    __tablename__ = "events"
    # TODO: add status ENUM: 0: Open, 1: Closed
    users = relationship(
        "User",
        secondary=user_event_association,
        back_populates="events",
    )
    min_players: Mapped[int] = mapped_column(Integer, default=10)
    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("locations.id"), nullable=False
    )
    location = relationship("Location", back_populates="events")


class Location(Base):
    __tablename__ = "locations"

    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    events = relationship("Event", back_populates="location")
