import logging

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import (
    Message,
)
from aiogram_calendar import SimpleCalendar, get_user_locale

from api_serv.api_service import (
    api_get_all_events,
    api_close_active_event,
    api_set_event_limit,
)
from src.config import settings

logging.basicConfig(level=logging.DEBUG, format=settings.logging.log_format)
logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.message(Command(commands=["new_game"]))
async def start_event(message: Message):
    locale = (
        await get_user_locale(message.from_user) if message.from_user else "ru"
    )
    calendar_kb = await SimpleCalendar(locale=locale).start_calendar()
    await message.answer(
        text="Когда игра?",
        reply_markup=calendar_kb,
    )


@router.message(Command(commands=["close"]))
async def close_events(message: Message, bot: Bot):
    chat_id = message.chat.id
    logger.debug("Try close in chat, %s", chat_id)
    await api_close_active_event(chat_id)

    original_text = "Foo"

    new_text = f"Завершено {original_text}"

    await bot.edit_message_text(
        chat_id=chat_id, message_id=msg_id, text=new_text
    )


@router.message(Command(commands=["list"]))
async def show_events(message: Message):
    games = await api_get_all_events()
    logger.debug("Got games %s", [g for g in games])
    if games:
        await message.answer(text=f"Есть {len(games)} игр.")

    else:
        await message.answer(text="Активных событий нет ✅")


@router.message(Command(commands=["limit"]))
async def set_event_limit(message: Message):
    limit = int(message.text.split(" ")[1])
    chat_id = message.chat.id
    if await api_set_event_limit(chat_id, limit):
        await message.answer(f"Минимальное количество игроков: {limit}")
    else:
        await message.answer("Не указано минимальное число игроков")
