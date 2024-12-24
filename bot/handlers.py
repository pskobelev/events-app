import logging
from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import (
    SimpleCalendar, get_user_locale,
    SimpleCalendarCallback
)

from api_service import api_add_new_event
from core.config import settings

logging.basicConfig(
    format=settings.logging.log_format,
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

URL = f"{settings.run.host}:{settings.run.port}{settings.api.prefix}"
user_router = Router(name=__name__)


@user_router.message(Command(commands=["new_game"]))
async def process_text_command(message: Message):
    """Start a new game"""
    chat_id = message.chat.id
    original_msg = message.text

    await message.answer(
        "Когда играем?",
        reply_markup=await SimpleCalendar(
            locale=await get_user_locale(message.from_user)).start_calendar()
    )


@user_router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery,
                                  callback_data: CallbackData):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query,
                                                      callback_data)
    chat_id = callback_query.message.chat.id
    if selected:
        params = {
            "event_name": "name",
            "chat_id":    chat_id,
            "event_date": date.isoformat(),
        }
        logger.info("User select date: %s, chat_id: %s", date, chat_id)

        if await api_add_new_event(params=params):
            logger.info("New event created successfully!")

        await callback_query.message.edit_text(
            f"⚽ Новая игра 🗓️{date.strftime("%d/%m/%Y")} ⚽",
        )
