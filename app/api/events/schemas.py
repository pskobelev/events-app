from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class EventBase(BaseModel):
    event_name: str
    chat_id: int
    event_date: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateEvent(EventBase):
    id: int


class UserEventCreate(BaseModel):
    user_id: int
    event_id: int
    username: str
    user_choice: str

    model_config = ConfigDict(from_attributes=True)
