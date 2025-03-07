import logging

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
    """return all active events in database"""
    result = await session.execute(select(Event).filter_by(active=True))
    return result.scalars().all()


async def get_active_event(event_id, chat_id, session):
    stmt = select(Event).where(
        and_(Event.chat_id == chat_id, Event.id == event_id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def update_event(event_id: int, session, **kwargs):
    stmt = update(Event).where(Event.id == event_id).values(**kwargs)
    await session.execute(stmt)
    await session.commit()


async def set_close_event(chat_id, session) -> None:
    stmt = (
        update(Event)
        .where(and_(Event.chat_id == chat_id, Event.active.is_(True)))
        .values(active=False)
    )  # noqa: E712
    await session.execute(stmt)
    logger.debug("Event closed")
    await session.commit()


async def set_delete_event(event_id: int, session):
    smtp = delete(Event).where(Event.id == event_id)
    await session.execute(smtp)
    await session.commit()


async def set_user_choice(data, session):
    user_dict = UserEvent(**(data.model_dump()))
    logger.debug("USER_DICT: %s", user_dict)
    stmt = select(UserEvent).where(
        and_(
            UserEvent.user_id == user_dict.user_id,
            UserEvent.event_id == user_dict.event_id,
        )
    )
    existing_user = (await session.execute(stmt)).scalar()
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


async def get_event_stat(event, session):
    stmt = select(UserEvent).where(UserEvent.event_id == event)
    result = await session.execute(stmt)
    result = result.scalars().all()
    return result


async def set_minimum_players(chat_id, limit, session):
    stmt = (
        update(Event).where(Event.id == chat_id).values(minimum_players=limit)
    )
    await session.execute(stmt)
    await session.commit()
