from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


class UserChoice(str, Enum):
    IN_GAME = "В игре ✅"
    PASS = "Пас ⛔"
    # THINKING = "Думаю 🫠"


class UserChoiceCbData(CallbackData, prefix="user-choice"):
    event_id: int
    choice: str


def build_action_kb(event_id, user_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for action in UserChoice:
        callback_data = UserChoiceCbData(
            event_id=event_id, choice=action.name
        ).pack()
        builder.button(text=action.value, callback_data=callback_data)
    # builder.adjust(1)
    if user_id == 722445:
        builder.button(text="Закрыть игру", callback_data="close_event")
    return builder.as_markup()


def build_admin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Закрыть игру", callback_data="close_event")
    return builder.as_markup()
