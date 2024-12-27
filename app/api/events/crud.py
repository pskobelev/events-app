import logging

from fastapi import HTTPException
from sqlalchemy import select, update, delete, and_

from app.models import Event
from models import UserEvent

logger = logging.getLogger(__name__)


async def create_new_event(event, session) -> Event:
    new_event = Event(**(event.model_dump()))
    session.add(new_event)
    await session.commit()
    await session.refresh(new_event)
    return new_event


async def get_active_events(session) -> dict:
    result = await session.execute(select(Event).filter_by(active=True))
    return result.scalars().first()


async def set_close_event(chat_id, session) -> None:
    stmt = (
        update(Event)
        .where(and_(Event.chat_id == chat_id, Event.active == True))
        .values(active=False)
    )  # noqa: E712
    await session.execute(stmt)
    logger.debug("Event closed")
    await session.commit()


async def get_active_event(event_id, chat_id, session):
    stmt = select(Event).where(
        chat_id=chat_id, event_id=event_id, session=session
    )
    await session.execute(stmt)
    await session.commit()


async def set_event_deleted(event_id, session):
    smtp = delete(Event).where(event_id == event_id).values(active=False)
    await session.execute(smtp)
    await session.commit()


async def set_user_choice(data, session):
    user_dict = UserEvent(**(data.model_dump()))
    query = select(UserEvent).where(
        and_(
            UserEvent.user_id == user_dict.user_id,
            UserEvent.event_id == user_dict.event_id,
        )
    )
    existing_user = (await session.execute(query)).scalar()
    if existing_user:
        logger.debug("OLD CHOICE: %s", existing_user.user_choice)
        logger.debug("NEW CHOICE: %s", user_dict.user_choice)
        existing_user.user_choice = user_dict.user_choice
        await session.commit()
    else:
        session.add(user_dict)
        await session.commit()
        await session.refresh(user_dict)
        return user_dict
    return user_dict or existing_user


async def crud_get_stats(event, session):
    query = select(UserEvent).where(UserEvent.event_id == event)
    result = await session.execute(query)
    result = result.scalars().all()
    return result


async def crud_get_active_events(chat_id, session):
    stmt = select(Event).where(Event.chat_id == chat_id)
    result = (await session.execute(stmt)).scalars().all()
    return result
