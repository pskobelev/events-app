from aiogram import Bot, Dispatcher

from app.bot.handlers import user_router
from app.core.config import get_config

config = get_config()
BOT_TOKEN = config.BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(user_router)


if __name__ == "__main__":
    dp.run_polling(bot)
