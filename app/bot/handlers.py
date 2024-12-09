from aiogram import Router
from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.utils import handle_response
from app.core.config import get_config
from core.utils import get_logger

logger = get_logger()
cfg = get_config()

URL = f"{cfg.API_PATH}"
user_router = Router(name=__name__)


@user_router.message(Command(commands=["start"]))
async def process_reg_command(message: Message):
    """Register a new user"""

    user_data = {
        "telegram_id": int(message.from_user.id),
        "name": message.from_user.first_name,
        "username": message.from_user.username,
    }
    logger.debug(f"user_data: {user_data}")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                    URL + "/users/add/", json=user_data
            ) as resp:
                try:
                    text = await handle_response(resp)
                    logger.debug(f"text: {text}")
                    await message.answer(f"Welcome!\n\n{text}")
                except ValueError as e:
                    logger.error("ValueError", e)
                    await message.answer(f"{e}")
        except Exception as e:
            logger.error(e)
            await message.reply(f"Unexpected error. \n{e}")


@user_router.message(Command(commands=["new_game"]))
async def process_text_command(message: Message):
    """Start a new game"""

    chat_id = message.chat.id
    logger.debug(chat_id)

    async with aiohttp.ClientSession() as session:
        async with session.post(
                URL + "/events/add/",
                json={"name": message.text, "chat_id": chat_id},
        ) as resp:
            logger.debug(resp)
            try:
                data = await handle_response(resp)
                logger.debug(data)
                await message.answer(f"Msg from database: {data}")
            except Exception as e:
                logger.error(e)
                await message.reply(f"Unexpected error. \n{e}")
