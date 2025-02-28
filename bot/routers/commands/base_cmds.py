import logging
from datetime import time, datetime

from api_srv.api_service import api_add_event

logger = logging.getLogger(__name__)


async def create_event(chat_id, event_date, event_time=time(10, 30)):
    event_date = datetime.combine(event_date, event_time)
    params = {
        "event_name": "⚽ИГРА",
        "chat_id": chat_id,
        "event_date": event_date.isoformat(),
    }
    logger.debug("User select date: %s, chat_id: %s", event_date, chat_id)
    new_event = await api_add_event(params=params)
    if new_event:
        logger.debug("New event created successfully!")
    return new_event
