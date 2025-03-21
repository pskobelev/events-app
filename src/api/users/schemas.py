from typing import Optional, Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    telegram_id: int = 12345
    name: Annotated[str, MinLen(1), MaxLen(20)] = "Людмил"
    username: Optional[str] = "Огурченко"
    model_config = ConfigDict(from_attributes=True)


class ViewUser(UserBase):
    telegram_id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
