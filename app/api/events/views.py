from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.events.crud import (
    create_new_event,
    set_close_event,
    get_active_events, get_active_event, set_event_deleted,
)
from api.events.schemas import EventBase
from core.utils import configure_logging
from db.db_helper import db_helper

logger = configure_logging()
router = APIRouter(prefix="/events", tags=["events"])


@router.post("/add/", response_model=list[EventBase])
async def add_event(event_in: EventBase,
                    session: AsyncSession = Depends(
                        db_helper.scoped_session_dependency)):
    query = await create_new_event(
        event=event_in, session=session
    )
    return query


@router.get("/", response_model=list[EventBase])
async def get_event(event_id, chat_id,
                    session: AsyncSession = Depends(
                        db_helper.scoped_session_dependency)):
    query = await get_active_event(
        event_id=event_id,
        chat_id=chat_id,
        session=session
    )
    return query


@router.get("/events", response_model=list[EventBase])
async def get_events(session: AsyncSession = Depends(
    db_helper.scoped_session_dependency)):
    query = await get_active_events(session=session)
    return query


@router.post("/close_event", response_model=list[EventBase])
async def close_event(session: AsyncSession = Depends(
    db_helper.scoped_session_dependency)):
    query = await set_close_event(session=session)
    return {"status": "closed", **query}


@router.delete("/events/{event_id}")
async def delete_event(event_id: int,
                       session: AsyncSession = Depends(
                           db_helper.scoped_session_dependency)):
    query = await set_event_deleted(event_id, session=session)
    return {"status": "deleted", **query}
