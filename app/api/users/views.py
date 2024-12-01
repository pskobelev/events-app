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
    result = await crud.get_all_users(db=db)
    return result


@router.get("/{telegram_id}", response_model=ViewUser)
async def get_spec_user(telegram_id: int, db: AsyncSession = Depends(get_session)):
    """Get a specific user"""
    result = await crud.get_user_info(db=db, telegram_id=telegram_id)
    return result


@router.post("/add/")
async def add_user(user: CreateUser, db: AsyncSession = Depends(get_session)):
    """
    Add a new user to the database.

    Args:
        user (CreateUser): The user data to be added.
        db (AsyncSession, optional): The database session dependency.

    Returns:
        dict: A dictionary containing the success status and the newly created user.
    """

    new_user = await crud.create_new_user(user_in=user, db=db)
    return new_user


@router.delete("/{telegram_id}")
async def delete_user(telegram_id: int, db: AsyncSession = Depends(get_session)):
    """
    Delete a user by their Telegram ID.

    Args:
        telegram_id (int): The Telegram ID of the user to be deleted.
        db (AsyncSession, optional): The database session dependency.

    Returns:
        dict: A dictionary indicating the success status of the deletion operation.
    """
    result = await crud.delete_user(db=db, telegram_id=telegram_id)
    return result
