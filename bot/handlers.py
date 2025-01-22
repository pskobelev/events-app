import logging
from datetime import datetime, time

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram_calendar import (
    SimpleCalendar,
    get_user_locale,
    SimpleCalendarCallback,
)

from api_service import (
    api_add_event,
    api_write_user_choice,
    api_get_event_stats,
    api_close_active_event,
)
from core.config import settings

logging.basicConfig(format=settings.logging.log_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)


user_router = Router(name=__name__)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/help"), KeyboardButton(text="/add_game")],
    ],
    resize_keyboard=True,
)


# Обработчик команды "/help"
@user_router.message(Command(commands=["help"]))
async def show_help(message: Message):
    help_text = """
    🤖 *Доступные команды*:
    - `/help` — описание команд и возможностей бота.
    - `/new_game` — добавить новую игру в расписание.
    - `/close` — завершить игру.
    """
    await message.answer(help_text, parse_mode="Markdown")


@user_router.message(Command(commands=["new_game"]))
async def process_text_command(message: Message):
    await message.answer(
        "Когда играем?",
        reply_markup=await SimpleCalendar(
            locale=await get_user_locale(message.from_user)
        ).start_calendar(),
    )


@user_router.message(Command(commands=["close"]))
async def process_close_command(message: Message):
    chat_id = message.chat.id
    logger.debug("Try close in chat, %s", chat_id)
    await api_close_active_event(chat_id)
    await message.answer('Активных событий нет.')


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
            "event_name": "Some name",
            "chat_id":    chat_id,
            "event_date": event_date.isoformat(),
        }
        logger.info("User select date: %s, chat_id: %s", event_date, chat_id)

        new_event = await api_add_event(params=params)
        if new_event:
            logger.info("New event created successfully!")

        logger.debug("New_event: %s", new_event)
        event_id = new_event.get("id")

        buttons = [
            InlineKeyboardButton(
                text="Играю ⚽", callback_data=f"uc_play:{event_id}"
            ),
            InlineKeyboardButton(
                text="Подумаю 🤔", callback_data=f"uc_maybe:{event_id}"
            ),
            InlineKeyboardButton(
                text="Не могу 🙅‍♂️", callback_data=f"uc_cannot:{event_id}"
            ),
        ]

        inline_kb = InlineKeyboardMarkup(
            inline_keyboard=[buttons],
        )

        await callback_query.message.edit_text(
            f"⚽ Новая игра 🗓️{event_date} ⚽",
            reply_markup=inline_kb,
        )


@user_router.callback_query(F.data.startswith("uc_"))
async def handle_game_buttons(callback_query: CallbackQuery):
    user_name = callback_query.from_user.full_name
    user_id = callback_query.from_user.id
    action, event_id = callback_query.data.split(":")
    logger.info("Start update message")
    params = {
        "user_id":  user_id,
        "username": user_name,
        "event_id": int(event_id),
        "user_choice": action,
    }
    logger.debug("User choice: %s", params)
    write_user = await api_write_user_choice(params=params)
    logger.debug("Write user choice: %s", write_user)
    event_users = await api_get_event_stats(int(event_id))
    logger.debug("Event users: %s", event_users)
    logger.debug("Event status: %s", event_users)

    # Формируем текст для обновленного сообщения
    playing = [
        user["username"]
        for user in event_users
        if user["user_choice"] == "uc_play"
    ]
    thinking = [
        user["username"]
        for user in event_users
        if user["user_choice"] == "uc_maybe"
    ]
    not_playing = [
        user["username"]
        for user in event_users
        if user["user_choice"] == "uc_cannot"
    ]

    logger.debug(
        "PLAYING: %s | THINKING: %s | NOT_PLAYING: %s",
        playing,
        thinking,
        not_playing,
    )

    message_text = f"""
⚽ Новая игра 🗓️ ⚽

Основной состав: {len(playing)} / 10:
{', '.join(playing) if playing else "Ты можешь быть первым"}

Скамейка: {len(thinking)}:
{', '.join(thinking) if thinking else "Хорошо подумай"}

Не играют - {len(not_playing)}:
{', '.join(not_playing) if not_playing else ""}
        """
    await callback_query.message.edit_text(
        message_text,
        reply_markup=callback_query.message.reply_markup,
    )
    logger.info("Message update SUCCESS!")
    # Уведомляем пользователя о выборе
    await callback_query.answer("")
