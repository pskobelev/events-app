from aiogram import Router
from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.utils import handle_response
from app.core.config import get_config
from core.utils import configure_logging

logger = configure_logging()
cfg = get_config()

URL = f"{cfg.API_PATH}"
user_router = Router(name=__name__)


@user_router.message(Command(commands=["start"]))
async def register_user(message: Message):
    user_data = {
        "telegram_id": int(message.from_user.id),
        "name": message.from_user.first_name,
        "username": message.from_user.username,
    }
    logger.info("user_data: %s", user_data)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(URL + "/users/add/",
                                    json=user_data) as resp:
                try:
                    text = await handle_response(resp)
                    logger.debug("AFTER reformat: %s", text)
                    await message.answer(f"Welcome!\n\n{text}")
                except ValueError as e:
                    logger.error("ValueError: %s", e)
                    await message.answer(f"{e}")
        except Exception as e:
            logger.exception("Get exception, %s", e)
            await message.reply(f"Unexpected error. \n{e}")


@user_router.message(Command(commands=["new_game"]))
async def process_text_command(message: Message):
    """Start a new game"""

    chat_id = message.chat.id
    logger.debug("Chat id: %s", chat_id)

    async with aiohttp.ClientSession() as session:
        try:

            async with session.post(
                    URL + "/events/add/",
                    json={"name": message.text, "chat_id": chat_id}, ) as resp:
                logger.debug("Request: %s", resp)
                try:
                    data = await handle_response(resp)
                    logger.debug("Handle data: %s", data)
                    await message.answer(f"Msg from database: {data}")
                except ValueError as e:
                    logger.error("Catch exception: %s", e)
        except Exception as e:
            logger.exception("Get exception, %s", e)
            await message.reply(f"Unexpected error. \n{e}")
