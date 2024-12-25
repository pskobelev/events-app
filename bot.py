import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError
from bot.handlers import user_router

from core.config import settings

logging.basicConfig(level=logging.INFO, format=settings.logging.log_format)

logger = logging.getLogger(__name__)
bot = Bot(token=settings.bot.token)
dp = Dispatcher()
dp.include_router(user_router)

if __name__ == "__main__":
    try:
        dp.run_polling(bot)
        logger.info("Bot is started!")

    except TelegramNetworkError:
        logger.exception(
            "Network Error",
            exc_info=False,
        )
