from fastapi import APIRouter

from api.events.crud import create_new_event
from api.events.schemas import EventBase
from core.utils import get_logger

router = APIRouter(prefix="/events", tags=["events"])
logger = get_logger()


@router.post("/add/")
async def add_event(event_in: EventBase):
    logger.debug(f"{event_in}")
    new_event = await create_new_event(event=event_in)
    return new_event
