from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users import crud
from app.api.users.schemas import CreateUser, ViewUser
from app.db.db_helper import get_session

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_user(db: AsyncSession = Depends(get_session)):
    """Read all users"""
    users_ = await crud.get_all_users(db=db)
    return users_


@router.post("/add/")
async def add_user(user: CreateUser, db: AsyncSession = Depends(get_session)):
    """Add a new user"""
    create_user = await crud.create_user(user_in=user, db=db)
    return create_user


@router.get("/{telegram_id}", response_model=ViewUser)
async def get_user(telegram_id: int, db: AsyncSession = Depends(get_session)):
    """Get a specific user"""
    spec_user = await crud.get_user_info(db=db, telegram_id=telegram_id)
    return spec_user
