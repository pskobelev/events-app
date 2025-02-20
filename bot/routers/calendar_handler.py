import logging
from datetime import datetime

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from aiogram_calendar import (
    SimpleCalendar,
    SimpleCalendarCallback,
    get_user_locale,
)

from api_srv.api_service import (
    api_get_event_stats,
    api_get_current_event, api_write_user_choice, )
from keyboard.user_choice_kb import build_action_kb, UserChoiceCbData
from routers.commands.base_cmds import create_event
from utils.format_message import format_date_with_day, edit_msg

logger = logging.getLogger(__name__)
router = Router(name=__name__)

DATE_FROM = datetime(2025, 1, 1)
DATE_TO = datetime(2025, 12, 31)


@router.callback_query(SimpleCalendarCallback.filter())
async def handle_calendar(
        callback_query: CallbackQuery,
        callback_data: CallbackData
):
    """ Show calendar for User """

    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user),
        show_alerts=True,
    )
    selected, event_date = await calendar.process_selection(
        callback_query,
        callback_data)

    if selected:
        new_event = await create_event(
            callback_query.message.chat.id,
            event_date)
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
    """ Handle user choice and write it to DB """

    user_name = callback_query.from_user.full_name
    user_id = callback_query.from_user.id
    choice = callback_data.choice
    event_id = callback_data.event_id

    params = {
        "user_id":     user_id,
        "username":    user_name,
        "event_id":    event_id,
        "user_choice": choice,
    }

    set_user_choice = await api_write_user_choice(params=params)
    logger.debug("User choice saved: %s", set_user_choice)

    current_event = await api_get_current_event(
        event_id,
        callback_query.message.chat.id,
    )

    title = current_event[0].get("event_name", "Default Event")
    event_time = current_event[0].get("event_date", 0)
    event_kb = build_action_kb(event_id)

    try:
        await callback_query.message.edit_text(
            text=(f"**{title}** {event_time}"
                  f"\n**{callback_query.message.text}**"),
            reply_markup=event_kb,
        )
    except Exception as e:
        logger.error("FAILED", e)
        await callback_query.message.answer('ERROR')

    # try:
    #     await update_event_message(callback_query, event_id)
    #     logger.debug("Update msg success!")
    # except Exception as e:
    #     logger.exception("FAILED, %s", e)
    # await callback_query.answer()


async def update_event_message(
        callback_query: CallbackQuery,
        event_id: int) -> str | None:
    """ Get Callback & event_id and update event message

    :param callback_query: CallbackQuery
    :param event_id: Event ID uniq for this chat
    :return: Event message or None
    """

    event_data = await api_get_event_stats(event_id)
    if not event_data:
        await callback_query.message.answer(
            text="Sorry, we couldn't find that event.", show_alert=True
        )
        return None
    logger.debug("Event STATS: %s", event_data)
    formatted_msg = "\n".join([msg.text for msg in await edit_msg(event_data)])

    event_dt = await api_get_current_event(
        event_id,
        callback_query.message.chat.id)
    logger.debug("Current EVENT: %s", event_dt)

    title = event_dt[0].get("event_name", "placeholder")
    date = await format_date_with_day(
        event_dt[0].get("event_date", "default date and time")
    )

    logger.debug("User click %s", callback_query.from_user.id)
    await callback_query.message.edit_text(
        text=f"{title} | {date}"
             f"\n{formatted_msg}",
    )
