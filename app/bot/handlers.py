from aiogram import Router
from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.utils import handle_response
from app.core.config import get_config
from core.utils import get_logger

logger = get_logger()

cfg = get_config()

URL = f"{cfg.API_PATH}/users/"
user_router = Router(name=__name__)


@user_router.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(f"I'm echo bot, write me something:\n{message.from_user}")


@user_router.message(Command(commands=["reg"]))
async def process_reg_command(message: Message):
    # Создаем словарь с данными пользователя
    user_data = {
        "telegram_id": int(message.from_user.id),
        "name": message.from_user.first_name,
        "username": message.from_user.username,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(URL + "add/", json=user_data) as resp:
                try:
                    text = await handle_response(resp)
                    await message.answer(f"Welcome {text}")
                except ValueError as e:
                    await message.answer(f"{e}")
        except Exception as e:
            logger.error(e)
            await message.reply(f"Unexpected error.")


@user_router.message(Command(commands=["users"]))
async def get_users(message: Message):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(URL) as resp:
                try:
                    text = await handle_response(resp)
                    logger.debug(f"Status Code: {resp.status}, URL: {URL}")

                    return await message.answer(text)
                except ValueError as e:
                    logger.error(f"ValueError: {e}, Status Code: {resp.status}, URL: {URL}")

                    await message.answer(f"Error: {e}")
        except Exception as e:
            logger.error(e)
            await message.reply(f"Error exception: {e}")


@user_router.message(Command(commands=["game"]))
async def process_game_command(message: Message):
    pass
