import logging

from sqlalchemy import select
from sqlalchemy.engine import Result

from models import User

logger = logging.getLogger(__name__)


async def create_new_user(user_in, session) -> User | None:
    new_user = User(**(user_in.model_dump()))
    if not await get_one_user_by_telegram_id(new_user.telegram_id):
        session.add(new_user)
        await session.commit()
        return new_user
    return None


async def get_all_users(session) -> list[User] | None:
    stmt = select(User).order_by(User.telegram_id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_one_user_by_telegram_id(telegram, session) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram)
    result: Result = await session.execute(stmt)
    logger.debug(f"Result: {result}")
    return result.scalars().first()
