from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    event_name: str
    chat_id: int
    model_config = ConfigDict(from_attributes=True)


class CreateEvent(EventBase):
    event_name: str


class UserEventCreate(BaseModel):
    user_id: int
    event_id: int

    model_config = ConfigDict(from_attributes=True)
