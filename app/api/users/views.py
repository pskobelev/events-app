from fastapi import APIRouter

from app.api.users import crud
from app.api.users.schemas import CreateUser

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/add_user/")
async def add_user(user: CreateUser):
    create_user = await crud.create_user(user_in=user)
    return create_user
