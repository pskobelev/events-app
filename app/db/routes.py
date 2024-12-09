from typing import Annotated

from annotated_types import MinLen, MaxLen
from fastapi import APIRouter

from app.core.config import get_config
from core.utils import get_logger

logger = get_logger()

config = get_config()
root_router = APIRouter(tags=["hello"])


@root_router.get("/")
async def hello() -> dict:
    return {"hello": "Hello, World!"}


@root_router.get("/{name}")
async def hello_name(name: Annotated[str, MinLen(3), MaxLen(10)]) -> dict:
    return {
        "hello": name,
        "name_len_is": len(name),
    }


logger.info("Routers load")
