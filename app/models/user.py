import enum

from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

user_event_association = Table(
    "user_event",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    extend_existing=True,
)

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    events = relationship(
        "Event",
        secondary=user_event_association,
        back_populates="users",
    )


class EventStatus(enum.Enum):
    NEW = "new"
    COMPLETED = "completed"


class Event(Base):
    __tablename__ = "events"
    __table_args__ = {'extend_existing': True}

    chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[EventStatus] = mapped_column(
        ENUM(EventStatus, name="event_status_enum"),
        default=EventStatus.NEW,
        nullable=False,
    )
    users = relationship(
        "User",
        secondary=user_event_association,
        back_populates="events",
    )
    min_players: Mapped[int] = mapped_column(
        Integer,
        default=10,
    )
    location_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("locations.id"),
        nullable=False,
    )
    location = relationship("Location", back_populates="events")


class Location(Base):
    __tablename__ = "locations"
    __table_args__ = {'extend_existing': True}
    
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        default="Москва",
    )
    events = relationship("Event", back_populates="location")
