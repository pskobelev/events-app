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
            text=button["text"],
            callback_data=f"uc_{button['choice']}:{event_id}",
        )
        for button in BUTTONS
    ]
    return InlineKeyboardMarkup(
        row_width=3, inline_keyboard=[buttons], resize_keyboard=True
    )
