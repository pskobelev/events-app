import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
)
from aiogram_calendar import SimpleCalendar, get_user_locale

from api_srv.api_service import api_get_all_events, api_close_active_event
from core.config import settings

logging.basicConfig(level=logging.DEBUG, format=settings.logging.log_format)
logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.message(Command(commands=["new_game"]))
async def start_event(message: Message):
    locale = await get_user_locale(message.from_user)
    calendar_kb = await SimpleCalendar(locale=locale).start_calendar()
    await message.answer(
        text="Когда игра?",
        reply_markup=calendar_kb,
    )


@router.message(Command(commands=["close"]))
async def close_events(message: Message):
    chat_id = message.chat.id
    logger.debug("Try close in chat, %s", chat_id)
    await api_close_active_event(chat_id)
    # TODO EB-49
    await message.answer("Активных событий нет.")



@router.message(Command(commands=["list"]))
async def show_events(message: Message):
    games = await api_get_all_events()
    logger.debug("Got games %s", [g for g in games])
    if games:
        await message.answer(text=f"Есть {len(games)} игр.")

    else:
        await message.answer(text="Активных событий нет ✅")
