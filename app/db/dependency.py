from fastapi import Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.crud import logger
from db.db_helper import db_helper
from models import User


async def get_one_user_by_telegram_id(
        telegram,
        session: AsyncSession = Depends(
            db_helper.scoped_session_dependency)) -> User:
    stmt = select(User).where(User.telegram_id == telegram)
    result: Result = await session.execute(stmt)
    logger.debug(f"Result: {result}")
    return result.scalars().first()
