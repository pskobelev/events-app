from typing import Optional, Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    telegram_id: int = 123
    name: Annotated[str, MinLen(3), MaxLen(20)] = "foo"
    username: Optional[str] = "bar"

    model_config = ConfigDict(from_attributes=True)


class CreateUser(UserBase):
    pass


class ViewUser(UserBase):
    telegram_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)