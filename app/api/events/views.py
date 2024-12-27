import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.events.crud import (
    set_user_choice,
    crud_get_stats,
    crud_get_active_events,
)
from api.events.schemas import CreateEvent
from app.api.events.crud import (
    create_new_event,
    set_close_event,
    set_event_deleted,
)
from app.api.events.schemas import EventBase, UserEventCreate
from app.db.db_helper import db_helper
from app.models import Event

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/events", tags=["events"])


@router.post("/add/", response_model=CreateEvent)
async def add_event(
        event_in: EventBase,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Event:
    query = await create_new_event(event=event_in, session=session)
    return query


@router.get("/events")
async def get_events(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    query = await find_active_events(session=session)
    return query


@router.post("/close_event/{chat_id}")
async def close_event(
        chat_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await set_close_event(chat_id, session=session)
    return {"status": "closed"}


@router.delete("/events/{event_id}")
async def delete_event(
        event_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    query = await set_event_deleted(event_id, session=session)
    return {"status": "deleted", **query}


@router.post("/user_choice/")
async def user_choice(
        user_data: UserEventCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    query = await set_user_choice(data=user_data, session=session)
    return query


@router.get("/stats/{event_id}")
async def get_stats(
        event_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    query = await crud_get_stats(event=event_id, session=session)
    return query


@router.get("/active_event/{chat_id}")
async def find_active_events(
        chat_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    query = await crud_get_active_events(chat_id, session=session)
    return query
