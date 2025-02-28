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


def build_action_kb(event_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for action in UserChoice:
        callback_data = UserChoiceCbData(
            event_id=event_id, choice=action.name
        ).pack()
        builder.button(text=action.value, callback_data=callback_data)
    # builder.adjust(1)
    return builder.as_markup()

# async def create_choice_keyboard(event_id: int) -> InlineKeyboardMarkup:
#     buttons = [
#         InlineKeyboardButton(
#             text=text, callback_data=f"uc_{choice}:{event_id}"
#         )
#         for choice, text in USER_CHOICES.items()
#     ]
#
#     return InlineKeyboardMarkup(
#         inline_keyboard=[buttons], row_width=3, resize_keyboard=True
#     )
