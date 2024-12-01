from typing import Any

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users.schemas import CreateUser, ViewUser
from app.db.db_helper import get_session
from app.models import User
from core.utils import get_logger

logger = get_logger()


async def create_new_user(
    user_in: CreateUser,
    db: AsyncSession = Depends(get_session),
) -> dict:
    # Преобразуем Pydantic-модель в словарь
    new_user = user_in.model_dump()

    existing_user = await get_user_info(db, user_in.telegram_id)
    if existing_user:
        logger.info(f"Find existing user: {existing_user.telegram_id}")
        raise HTTPException(
            status_code=400,
            detail="User already exists",
        )

    # Создаем объект SQLAlchemy
    db_user = User(**new_user)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {
        "success": True,
        "user": db_user,
    }


async def get_user_info(db: AsyncSession, telegram_id: int) -> Any:
    """
    Find user by telegram id
    :param db:
    :param telegram_id:
    :return:
    """

    logger.debug(f"Telegram ID: {telegram_id}")
    query = select(User).where(User.telegram_id == telegram_id)
    result = await db.execute(query)
    user = result.scalars().first()
    if user:
        return user
    else:
        return None


async def get_all_users(db: AsyncSession) -> Any:
    result = await db.execute(select(User))
    scalars__all = result.scalars().all()
    return [ViewUser.model_validate(user) for user in scalars__all]


async def delete_user(db: AsyncSession, telegram_id: int) -> dict:
    logger.debug(f"Start delete user: {telegram_id}")
    query = select(User).where(User.telegram_id == telegram_id)
    result = await db.execute(query)
    user = result.scalars().first()
    if user:
        await db.delete(user)
        await db.commit()
        logger.debug(f"Deleted user: {telegram_id} complete")
        return {"success": True}
    else:
        logger.debug(f"User not found: {telegram_id}")
        return {"success": False}
