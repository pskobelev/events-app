from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError

from app.bot.handlers import user_router
from app.core.config import get_config
from app.core.utils import configure_logging

logger = configure_logging()
config = get_config()

BOT_TOKEN = config.BOT_TOKEN

logger.info("Loading bot...")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(user_router)
logger.info("Bot is started!")

if __name__ == "__main__":
    try:
        dp.run_polling(bot)
    except TelegramNetworkError:
        logger.exception("Network Error", exc_info=False, )
