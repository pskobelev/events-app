from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

BUTTONS = [
    {"text": "В игре ✅", "choice": "in_game"},
    {"text": "Пас ⛔", "choice": "pass"},
    {"text": "Думаю 🫠", "choice": "thinking"},
]

MENU_CMD = [
    BotCommand(command="new_game", description="Start a new game"),
    BotCommand(command="close", description="Finish active game"),
    BotCommand(command="foo", description="Bar"),
    BotCommand(command="list", description="List games"),
]


async def set_user_choice_kb(event_id):
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
    return InlineKeyboardMarkup(
        row_width=3, inline_keyboard=[buttons], resize_keyboard=True
    )
