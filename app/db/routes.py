from fastapi import APIRouter

from app.core.config import get_config

config = get_config()
root_router = APIRouter(tags=["hello"])


@root_router.get("/")
async def hello() -> dict:
    return {"hello": "Hello, World!"}
