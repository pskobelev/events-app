from fastapi import HTTPException
from sqlalchemy import select, update, delete

from core.utils import configure_logging
from models import Event

logger = configure_logging()


async def create_new_event(event, session) -> dict:
    new_event = Event(**(event.model_dump()))
    if not await get_active_events(session):
        session.add(new_event)
        await session.commit()
        await session.refresh(new_event)
        return {
            "success": True,
        }
    raise HTTPException(status_code=400, detail="Event already exists")


async def get_active_events(session) -> dict:
    result = await session.execute(select(Event).filter_by(active=True))
    return result.scalars().first()


async def set_close_event(session) -> None:
    stmt = update(Event).where(Event.active == True).values(
        active=False)  # noqa: E712
    await session.execute(stmt)
    await session.commit()


async def get_active_event(event_id, chat_id, session):
    stmt = select(Event).where(chat_id=chat_id, event_id=event_id,
                               session=session)
    await session.execute(stmt)
    await session.commit()


async def set_event_deleted(event_id, session):
    smtp = delete(Event).where(event_id == event_id).values(active=False)
    await session.execute(smtp)
    await session.commit()
