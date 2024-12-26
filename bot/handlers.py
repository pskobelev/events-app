import logging
from datetime import datetime, time
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup, )
from aiogram_calendar import (
    SimpleCalendar,
    get_user_locale,
    SimpleCalendarCallback,
)

from api_service import api_add_new_event
from core.config import settings

logging.basicConfig(format=settings.logging.log_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)

URL = f"{settings.api.host}:{settings.run.port}"
user_router = Router(name=__name__)


@user_router.message(Command(commands=["new_game"]))
async def process_text_command(message: Message):
    await message.answer(
        "Когда играем?",
        reply_markup=await SimpleCalendar(
            locale=await get_user_locale(message.from_user)
        ).start_calendar(),
    )


@user_router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(
        callback_query: CallbackQuery, callback_data: CallbackData
):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user),
        show_alerts=True,
    )
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(
        callback_query, callback_data
    )
    chat_id = callback_query.message.chat.id
    if selected:
        default_time = time(10, 30)
        event_date = datetime.combine(date, default_time)
        params = {
            "event_name": "name",
            "chat_id":    chat_id,
            "event_date": event_date.isoformat(),
        }
        logger.info("User select date: %s, chat_id: %s", event_date, chat_id)

        if await api_add_new_event(params=params):
            logger.info("New event created successfully!")

        buttons = [
            InlineKeyboardButton(text="Играю ⚽", callback_data="play"),
            InlineKeyboardButton(text="Подумаю 🤔", callback_data="maybe"),
            InlineKeyboardButton(text="Не могу 🙅‍♂️", callback_data="cannot"),
        ]

        inline_kb = InlineKeyboardMarkup(
            inline_keyboard=[buttons],
        )

        await callback_query.message.edit_text(
            f"⚽ Новая игра 🗓️{event_date} ⚽",
            reply_markup=inline_kb,
        )


cd_data = ['play', 'maybe', 'cannot']


# <editor-fold desc="Callback for inline buttons">
@user_router.callback_query(F.cd_data)
async def handle_game_buttons(callback_query: CallbackQuery):
    user_name = callback_query.from_user.full_name

    responses = {
        "play":   f"✅ {user_name} идет играть!",
        "maybe":  f"🤔 {user_name} подумает.",
        "cannot": f"❌ {user_name} не сможет прийти.",
    }

    # Редактируем сообщение с новым текстом

    await callback_query.message.edit_text('a',
                                           reply_markup=callback_query.message.reply_markup)

    # Уведомляем пользователя о выборе
    await callback_query.answer("Ваш выбор записан!")
# </editor-fold>
