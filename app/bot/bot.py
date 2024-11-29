import logging

from aiogram import Bot, Dispatcher

from app.core.config import get_config

cfg = get_config()

BOT_TOKEN = str(cfg.BOT_TOKEN)

URL = f"{cfg.API_PATH}/users/"

logging.basicConfig(
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

if __name__ == "__main__":
    dp.run_polling(bot)
