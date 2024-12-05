from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class CreateEvent(EventBase):
    pass


class ViewEvent(EventBase):
    pass
