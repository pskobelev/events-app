from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.crud import (
    get_all_users, create_new_user,
)
from api.users.schemas import ViewUser, UserBase
from core.utils import configure_logging
from db.db_helper import db_helper

logger = configure_logging()
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/all_users", response_model=list[ViewUser])
async def get_users(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await get_all_users(session=session)


@router.post("/add/", response_model=ViewUser,
             status_code=status.HTTP_201_CREATED,
             )
async def add_user(user_in: UserBase,
                   session: AsyncSession = Depends(
                       db_helper.scoped_session_dependency)):
    new_user = await create_new_user(user_in=user_in, session=session)
    return new_user

# @router.get("/{telegram_id}", response_model=list[ViewUser])
# async def get_user(telegram_id: int, session):
#     user = await get_one_user_by_telegram_id(telegram_id, session)
#     if not user:
#         raise HTTPException(
#             status.HTTP_404_NOT_FOUND, detail=f"User {telegram_id} not found"
#         )
#     return user
#
#
#
#     # if not new_user:
#     #     raise HTTPException(
#     #         status.HTTP_208_ALREADY_REPORTED, detail="User already exists"
#     #     )
