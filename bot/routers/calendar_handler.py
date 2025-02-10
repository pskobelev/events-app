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
from keyboard.user_choice_kb import (create_choice_keyboard, build_action_kb,
                                     UserChoiceCbData)
from utils.edit_event_message import edit_msg, format_date_with_day

logger = logging.getLogger(__name__)

router = Router(name=__name__)

DATE_FROM = datetime(2025, 1, 1)
DATE_TO = datetime(2025, 12, 31)


@router.callback_query(SimpleCalendarCallback.filter())
async def show_calendar(
        callback_query: CallbackQuery, callback_data: CallbackData
):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user),
        show_alerts=True,
    )
    calendar.set_dates_range(DATE_FROM, DATE_TO)
    selected, event_date = await calendar.process_selection(
        callback_query, callback_data
    )

    chat_id = callback_query.message.chat.id

    if selected:
        new_event = await create_event(chat_id, event_date)
        event_id = new_event.get("id")
        date_with_day = await format_date_with_day(event_date.isoformat())

        event_msg = new_event.get("event_name") + date_with_day
        user_choice_kb = await create_choice_keyboard(event_id)

        new_kb = build_action_kb()
        await callback_query.message.edit_text(
            event_msg,
            reply_markup=new_kb,
        )


@router.callback_query(UserChoiceCbData.filter())
async def handle_user_choice(
        callback_query: CallbackQuery,
        callback_data: UserChoiceCbData
):
    await callback_query.answer(
        text=(
            f"You chose: {callback_data.choice}\n"
            f"Callback {callback_query.data!r}")
    )


@router.callback_query(UserChoiceCbData.filter())
async def handle_buttons(callback_query: CallbackQuery):
    user_name = callback_query.from_user.full_name
    user_id = callback_query.from_user.id
    action, event_id = callback_query.data.split(":")
    logger.debug("Start update message")
    params = {
        "user_id":  user_id,
        "username": user_name,
        "event_id": int(event_id),
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

    updated_msg = await edit_msg(event_data)
    msg = {
        "event_name": ev_name,
        "event_date": date_with_day,
    }

    # msg = f"{ev_name} {date_with_day}\n\n{msg}"

    await callback_query.message.edit_text(
        **updated_msg.as_kwargs(),
        reply_markup=callback_query.message.reply_markup,
    )


async def create_event(chat_id, event_date, event_time=time(10, 30)):
    event_date = datetime.combine(event_date, event_time)
    params = {
        "event_name": "⚽ИГРАЕМ",
        "chat_id": chat_id,
        "event_date": event_date.isoformat(),
    }
    logger.debug("User select date: %s, chat_id: %s", event_date, chat_id)
    new_event = await api_add_event(params=params)
    if new_event:
        logger.debug("New event created successfully!")
    return new_event
