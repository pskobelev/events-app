from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class EventBase(BaseModel):
    event_name: str
    chat_id: int
    event_date: datetime

    # @field_validator("event_date", mode="before")
    # def parse_event_date(cls, value):
    #     if isinstance(value, str):
    #         # Преобразуем строку формата "YYYY-MM-DD HH:MM" в datetime
    #         return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    #     return value

    model_config = ConfigDict(from_attributes=True)


class CreateEvent(EventBase):
    id: int


class UserEventCreate(BaseModel):
    user_id: int
    event_id: int
    user_choice: str

    model_config = ConfigDict(from_attributes=True)
