import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError

from core.config import settings
from keyboard.main_kb import MENU_CMD
from routers import router as main_router

logging.basicConfig(level=logging.DEBUG, format=settings.logging.log_format)
logger = logging.getLogger(__name__)


async def set_commands(bt: Bot):
    await bt.set_my_commands(MENU_CMD)


async def main():
    dp = Dispatcher()
    dp.include_router(main_router)
    bot = Bot(token=settings.bot.token)

    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        logger.info("🤖I'm alive!")
    except TelegramNetworkError:
        logger.exception(
            "Network Error",
            exc_info=False,
        )
