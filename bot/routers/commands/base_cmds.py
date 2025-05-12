import logging
import random
from datetime import time, datetime

from api_serv.api_service import api_add_event

logger = logging.getLogger(__name__)


async def create_event(
    chat_id, event_date, event_time=time(10, 30)
) -> dict[str, str]:
    event_date = datetime.combine(event_date, event_time)
    game_name = f"⚽{get_random_football_name()}"
    params = {
        "event_name": game_name,
        "chat_id": chat_id,
        "event_date": event_date.isoformat(),
    }
    logger.debug("User select date: %s, chat_id: %s", event_date, chat_id)
    new_event = await api_add_event(params=params)
    if new_event:
        logger.debug("New event created successfully!")
    return new_event


def get_random_football_name():
    names = [
        "Прод упал, но мы держимся",
        "Откатим, если не зайдет",
        "Git Revert FC",
        "А где тесты?",
        "Деплой на прод перед матчем",
        "WARNING не ошибка, играем",
        "500: Вратарь не отвечает",
        "Мерж-конфликт на поле",
        "DevOps не пинает просто так",
        "Весь спринт в защите",
        "Отладка на поле",
        "Тикет закрыл, гол забил",
    ]

    name = random.choice(names)
    return name
