from fastapi import APIRouter

from app.config import get_config

config = get_config()
root_router = APIRouter()


@root_router.get("/")
async def hello() -> dict:
    return {"hello": "Hello, World!"}
