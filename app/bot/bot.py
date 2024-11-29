import json
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = "6099320295:AAGxPr4gnnQu35SEAKqiTns0GJQSVr0Z9mY"
URL = "http://127.0.0.1:8000/users/"

logging.basicConfig(
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        f"I'm echo bot, write me something:\n{message.from_user}"
    )


@dp.message(Command(commands=["reg"]))
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


@dp.message(Command(commands=["users"]))
async def get_users(message: Message):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(URL) as resp:
                try:
                    text = await handle_response(resp)
                    return await message.answer(text)
                except ValueError as e:
                    logger.error(f"ValueError: {e}")
                    await message.answer(f"Error: {e}")
        except Exception as e:
            logger.error(e)
            await message.reply(f"Error exception: {e}")


async def format_text(msg):
    formatted_msg = json.dumps(msg, indent=2)
    return formatted_msg


async def handle_response(resp):
    """
    Handle and format response from server
    """
    if resp.status == 200:
        data = await resp.json()
        return await format_text(data)
    else:
        error_data = await resp.json()
        error_text = await format_text(error_data)
        raise ValueError(
            f"Server responded with an error: {resp.status}, {error_text}"
        )


if __name__ == "__main__":
    dp.run_polling(bot)
