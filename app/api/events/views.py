from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.events.crud import create_event
from api.events.schemas import CreateEvent
from db.db_helper import get_session

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/")
async def get_events(db):
    """Returns all events"""
    pass


@router.post("/add")
async def add_event(
        event: CreateEvent, db: AsyncSession = Depends(get_session)
):
    result = await create_event(event, db=db, event_in=event)
    return result


@router.delete("/delete")
async def delete_event(event, db):
    """
    Функция для удаления события из базы данных.

    Args:
        event: Объект, представляющий событие, которое нужно удалить.
        db: Объект, представляющий базу данных, из которой нужно удалить событие.

    Returns:
        None
    """
    pass
