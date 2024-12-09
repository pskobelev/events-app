from core.utils import get_logger
from db.db_helper import connection
from models import Event

logger = get_logger()


@connection
async def create_new_event(event, session) -> dict:
    new_event = Event(**(event.model_dump()))
    logger.debug(f"New_event: {new_event}")
    session.add(new_event)
    await session.commit()
    await session.refresh(new_event)
    return {
        'success': True,
    }
