from api.users.crud import (
    create_new_user, get_all_users, get_user_by_telegram_id
)
from api.users.schemas import UserBase, ViewUser
from core.utils import get_logger
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/users", tags=["users"])
logger = get_logger()


@router.post("/add/")
async def add_user(user: UserBase):
    new_user = await create_new_user(user_in=user)
    if new_user:
        return new_user
    raise HTTPException(201, detail="User already exists")


@router.get("/{telegram_id}")
async def get_user(telegram_id: int):
    id_ = await get_user_by_telegram_id(telegram_id)
    if id_:
        return ViewUser.model_validate(id_)
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/all_users")
async def get_users():
    result = await get_all_users()
    for i in result:
        user_res = ViewUser.model_validate(i)
        return user_res.model_dump()
