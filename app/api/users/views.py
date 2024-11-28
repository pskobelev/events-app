from fastapi import APIRouter

from app.api.users import crud
from app.api.users.crud import get_all_users
from app.api.users.schemas import CreateUser

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/add_user/")
async def add_user(user: CreateUser):
    create_user = await crud.create_user(user_in=user)
    return create_user


@router.get("/get_user/")
async def get_user():
    return get_all_users()
