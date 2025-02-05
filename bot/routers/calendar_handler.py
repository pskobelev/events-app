import logging
from datetime import datetime, time

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram_calendar import (
    SimpleCalendar,
    get_user_locale,
    SimpleCalendarCallback,
)

from api_srv.api_service import (
    api_write_user_choice,
    api_get_event_stats,
    api_get_current_event,
    api_add_event,
)
from keyboard.main_kb import set_user_choice_kb
from utils.edit_event_message import edit_msg, format_date_with_day

logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.callback_query(SimpleCalendarCallback.filter())
async def show_calendar(
        callback_query: CallbackQuery, callback_data: CallbackData
):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user),
        show_alerts=True,
    )
    calendar.set_dates_range(datetime(2025, 1, 1), datetime(2025, 12, 31))
    selected, event_date = await calendar.process_selection(
        callback_query, callback_data
    )

    chat_id = callback_query.message.chat.id

    if selected:
        new_event = await create_event(chat_id, event_date)
        event_id = new_event.get("id")
        date_with_day = await format_date_with_day(event_date.isoformat())
        event_msg = new_event.get("event_name") + date_with_day
        user_choice_kb = await set_user_choice_kb(event_id)

        await callback_query.message.edit_text(
            event_msg,
            reply_markup=user_choice_kb,
        )


@router.callback_query(F.data.startswith("uc_"))
async def handle_buttons(callback_query: CallbackQuery):
    user_name = callback_query.from_user.full_name
    user_id = callback_query.from_user.id
    action, event_id = callback_query.data.split(":")
    logger.info("Start update message")
    params = {
        "user_id":     user_id,
        "username":    user_name,
        "event_id":    int(event_id),
        "user_choice": action,
    }
    set_user_choice = await api_write_user_choice(params=params)
    logger.debug("User choice: %s", set_user_choice)
    event_data = await api_get_event_stats(int(event_id))

    logger.debug("Event users: %s", event_data)

    cur_event = await api_get_current_event(
        int(event_id), chat_id=callback_query.message.chat.id
    )

    ev_name = cur_event[0].get("event_name")
    ev_date = cur_event[0].get("event_date")

    # TODO: replace event_data > ev_date
    date_with_day = await format_date_with_day(ev_date)

    logger.debug("API_GET_CURRENT_EVENT: %s", date_with_day)

    message_text = (
            ev_name + date_with_day + "\n\n" + await edit_msg(event_data)
    )

    await callback_query.message.edit_text(
        message_text,
        reply_markup=callback_query.message.reply_markup,
    )


async def create_event(chat_id, event_date, event_time=time(10, 30)):
    event_date = datetime.combine(event_date, event_time)
    params = {
        "event_name": "⚽ИГРАЕМ",
        "chat_id":    chat_id,
        "event_date": event_date.isoformat(),
    }
    logger.debug("User select date: %s, chat_id: %s", event_date, chat_id)
    new_event = await api_add_event(params=params)
    if new_event:
        logger.debug("New event created successfully!")
    return new_event
