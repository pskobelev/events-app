from typing import Annotated

from annotated_types import MinLen, MaxLen
from fastapi import APIRouter

from app.core.config import get_config
from core.fake_data import generate_users
from core.utils import configure_logging

logger = configure_logging()

config = get_config()
root_router = APIRouter(tags=["hello"])


@root_router.get("/")
async def hello() -> dict:
    return {"hello": "Hello, World!"}


@root_router.get("/users")
async def get_users() -> dict:
    users = generate_users()
    return {"users": users}

@root_router.get("/{name}")
async def hello_name(name: Annotated[str, MinLen(3), MaxLen(10)]) -> dict:
    return {
        "hello": name,
        "name_len_is": len(name),
    }

