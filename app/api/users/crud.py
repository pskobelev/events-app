from typing import Any

from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users.schemas import CreateUser
from app.models import User
from app.db.database import get_session


async def create_user(
    user_in: CreateUser,
    db: AsyncSession = Depends(get_session),
) -> dict:
    new_user = user_in.model_dump()
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {
        "success": True,
        "user": new_user,
    }


# get users
async def get_all_users(db: AsyncSession = Depends(get_session)) -> Any:
    users = select(User)
    result = await db.execute(users)
    return result.scalars().all()
