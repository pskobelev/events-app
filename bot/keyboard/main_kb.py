from aiogram.types import (
    BotCommand,
)

# Команды меню бота
MENU_COMMANDS = [
    BotCommand(command="new_game", description="Создать новую игру"),
    BotCommand(command="close", description="Закрыть активную игру"),
    BotCommand(command="list", description="Список игр"),
]
