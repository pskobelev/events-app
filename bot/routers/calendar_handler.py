import logging
from datetime import datetime

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_calendar import (
    SimpleCalendar,
    SimpleCalendarCallback,
    get_user_locale,
)
from aiogram.enums import ParseMode

from api_srv.api_service import (
    api_get_current_event,
    api_write_user_choice,
)
from keyboard.user_choice_kb import build_action_kb, UserChoiceCbData
from routers.commands.base_cmds import create_event
from utils.format_message import format_date_with_day, update_event_message

logger = logging.getLogger(__name__)
router = Router(name=__name__)

DATE_FROM = datetime(2025, 1, 1)
DATE_TO = datetime(2025, 12, 31)


@router.callback_query(SimpleCalendarCallback.filter())
async def handle_calendar(
        callback_query: CallbackQuery, callback_data: SimpleCalendarCallback
):
    """Show calendar for User"""
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user),
        show_alerts=True,
    )
    selected, event_date = await calendar.process_selection(
        callback_query, callback_data
    )

    if selected:
        new_event = await create_event(
            callback_query.message.chat.id, event_date
        )
        event_id = new_event.get("id")
        date_with_day = await format_date_with_day(event_date.isoformat())
        event_msg = new_event.get("event_name") + date_with_day

        # Показываем кнопки для голосования
        event_kb = build_action_kb(event_id)
        await callback_query.message.edit_text(
            event_msg, reply_markup=event_kb
        )


@router.callback_query(UserChoiceCbData.filter())
async def handle_user_choice(
        callback_query: CallbackQuery, callback_data: UserChoiceCbData
):
    """Handle user choice and write it to DB"""

    user_name = callback_query.from_user.full_name
    user_id = callback_query.from_user.id
    choice = callback_data.choice
    event_id = callback_data.event_id
    chat_id = callback_query.message.chat.id

    params = {
        "user_id":  user_id,
        "username": user_name,
        "event_id": event_id,
        "user_choice": choice,
    }

    is_active = await api_get_current_event(event_id, chat_id)

    if is_active[0].get("active"):
        logger.debug("Current event: %s is active %s", event_id, is_active)

        set_user_choice = await api_write_user_choice(params=params)
        logger.debug("Write user choice to DB: %s", set_user_choice)
        event_kb = build_action_kb(event_id)

        event_date = is_active[0].get("event_date", 0)
        event_formated_date = await format_date_with_day(event_date)

        event_title = is_active[0].get("event_name", "Default Event")

        footer_text = (
            await update_event_message(callback_query, event_id)
        ).as_html()
        logger.debug("updated as string: %s", footer_text)

        full_text = f"{event_title} {event_formated_date}\n\n{footer_text}"
        try:
            await callback_query.message.edit_text(
                full_text,
                reply_markup=event_kb,
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:
            logger.error("FAILED", e)
            await callback_query.message.answer("")
    else:
        logger.debug("Current event: %s is not active", event_id)
        await callback_query.message.reply("Событие уже не активно.")
