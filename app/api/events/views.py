import logging

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.events.crud import (
    set_user_choice,
    get_event_stat,
    get_active_events,
    get_active_event,
    set_delete_event,
    set_close_event,
    set_minimum_players,
)
from api.events.schemas import EventCreate
from app.api.api_routes import ApiRoutes
from app.api.events.crud import (
    create_new_event,
)
from app.api.events.schemas import EventBase, UserEventCreate
from app.db.db_helper import db_helper
from app.models import Event

logger = logging.getLogger(__name__)
router = APIRouter(prefix=ApiRoutes.EVENT_BASE, tags=["events"])


@router.post(ApiRoutes.ADD_EVENT, response_model=EventCreate)
async def add_event(
    event_in: EventBase,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Event:
    query = await create_new_event(event=event_in, session=session)
    return query


@router.get(ApiRoutes.LIST_EVENT)
async def get_events(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    query = await get_active_events(session=session)
    if query is None:
        raise HTTPException(status_code=404)
    return query


@router.post(ApiRoutes.CLOSE_EVENT)
async def close_event(
    chat_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await set_close_event(chat_id, session=session)
    return {"chat_id": chat_id, "status": "closed"}


@router.delete(ApiRoutes.DELETE_EVENT)
async def delete_event(
    event_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await set_delete_event(event_id, session=session)
    return {"status": "deleted"}


@router.post(ApiRoutes.USER_CHOICE)
async def user_choice(
    user_data: UserEventCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    query = await set_user_choice(data=user_data, session=session)
    return query


@router.get(ApiRoutes.STATS)
async def get_stats(
    event_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    query = await get_event_stat(event=event_id, session=session)
    return query


@router.get(ApiRoutes.FIND_EVENT)
async def find_active_events(
    chat_id: int,
    event_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    query = await get_active_event(
        chat_id=chat_id, event_id=event_id, session=session
    )
    return query


# @router.post(ApiRoutes.LIMIT)
# async def set_limit_event(
#     chat_id: int,
#     limit: int,
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ) -> dict[str:str]:
#     query = await set_minimum_players(
#         chat_id=chat_id, limit=limit, session=session
#     )
#     return query
