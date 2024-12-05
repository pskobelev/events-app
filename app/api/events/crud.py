from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.events.schemas import CreateEvent
from core.utils import get_logger
from db.db_helper import get_session
from models import Event

log = get_logger()


async def create_event(
        msg,
        event_in: CreateEvent,
        db: AsyncSession = Depends(get_session()),
):
    """Create a new event."""
    new_event = msg.model_dump()
    log.debug(new_event)
    new_event = Event(**new_event)
    log.debug(new_event)
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return {
        "status":   "ok",
        "event_id": new_event.id,
    }


async def event_cancel(
        db: AsyncSession = Depends(get_session()),
):
    """Cancel an event."""
    pass
