from sqlalchemy import select

from app.core.utils import get_logger
from db.db_helper import connection
from models import User

logger = get_logger()


@connection
async def create_new_user(user_in, session) -> dict:
    new_user = User(**(user_in.model_dump()))
    if not await get_user_by_telegram_id(new_user.telegram_id):
        session.add(new_user)
        await session.commit()
        return {
            "success": True,
            "data":    new_user.id,
        }


@connection
async def get_all_users(session) -> dict:
    query = select(User)
    result = await session.execute(query)
    records = result.scalars().all()
    return records


@connection
async def get_user_by_telegram_id(telegram_id: int, session) -> dict:
    query = select(User).filter_by(telegram_id=telegram_id)
    result = await session.execute(query)
    return result.scalars().first()
