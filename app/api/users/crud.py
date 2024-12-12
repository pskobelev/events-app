from sqlalchemy import select
from sqlalchemy.engine import Result

from db.dependency import get_one_user_by_telegram_id
from models import User
from core.utils import configure_logging

logger = configure_logging()


async def create_new_user(user_in, session) -> User:
    new_user = User(**(user_in.model_dump()))
    if not await get_one_user_by_telegram_id(new_user.telegram_id):
        session.add(new_user)
        await session.commit()
        return new_user


async def get_all_users(session) -> list[User]:
    stmt = select(User).order_by(User.telegram_id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_one_user_by_telegram_id(telegram, session) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram)
    result: Result = await session.execute(stmt)
    logger.debug(f"Result: {result}")
    return result.scalars().first()

# 827816
