from typing import Any

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users.schemas import CreateUser, ViewUser
from app.db.db_helper import get_session
from app.models import User


async def create_user(
    user_in: CreateUser,
    db: AsyncSession = Depends(get_session),
) -> dict:
    # Преобразуем Pydantic-модель в словарь
    new_user = user_in.model_dump()

    query = select(User).where(User.telegram_id == new_user["telegram_id"])
    result = await db.execute(query)
    existing_user = result.scalars().first()
    if existing_user:
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


async def get_all_users(db: AsyncSession) -> Any:
    result = await db.execute(select(User))
    scalars__all = result.scalars().all()
    return [ViewUser.model_validate(user) for user in scalars__all]
