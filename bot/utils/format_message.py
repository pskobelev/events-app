import logging
from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram.utils.formatting import (
    Bold,
    Text,
    as_numbered_list,
    as_section,
)

from api_srv.api_service import api_get_event_stats

logger = logging.getLogger(__name__)


async def update_event_message(callback_query: CallbackQuery, event_id: int):
    """Get Callback & event_id and update event message

    :param callback_query: CallbackQuery
    :param event_id: Event ID uniq for this chat
    :return: Event message or None
    """

    event_data = await fetch_event_data(event_id)
    if not event_data:
        await handle_missing_event(callback_query)
        return None

    message = await update_footer_msg(event_data)
    return message


async def update_footer_msg(event_data):
    categories = {
        "Основной состав:": ("IN_GAME", "👟 "),
        "Скамейка:":   ("THINKING", "🔁 "),
        "Отказались:": ("PASS", "❌ "),
    }
    content = Text()
    # todo: изменить логику, тк сейчас не обрабатывается случай, когда на игру установлено минимальное число игроков
    # если количество игроков набирается, то остальные должны попадать в секцию "скамейка"
    for category, (status, emoji) in categories.items():
        players = [
            player.get("username", "Unknown")
            for player in event_data
            if player.get("user_choice") == status
        ]
        if players:
            section = as_section(
                Bold(f"{emoji}{category}"), as_numbered_list(*players), "\n\n"
            )
            content = Text(content, section)
    logger.debug("CONTENT as_kwargs(): %s", content.as_kwargs())

    return content


async def fetch_event_data(event_id: int) -> dict | None:
    """Fetch event data from API"""
    try:
        event_data = await api_get_event_stats(event_id)
        if not event_data:
            return None
        return event_data
    except Exception as e:
        logger.error("FAILED", e)
        return None


async def handle_missing_event(callback_query: CallbackQuery):
    await callback_query.message.answer(
        "Sorry, I couldn't find that event.", show_alerts=True
    )


async def format_date_with_day(event_date):
    date = datetime.fromisoformat(event_date)
    date_with_day = f"🗓️ {date.date().isoformat()} ({date.strftime('%A')})"
    return date_with_day
