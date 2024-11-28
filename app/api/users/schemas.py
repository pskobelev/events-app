from typing import Optional, Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    pass


class CreateUser(UserBase):
    """Pydantic user model."""

    telegram_id: int
    name: Annotated[str, MinLen(3), MaxLen(20)]
    username: Optional[str] = None
    # config = ConfigDict(from_attributes=True)
