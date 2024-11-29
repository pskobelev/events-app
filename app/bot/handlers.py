from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.bot import dp, URL, logger
from app.bot.utils import handle_response


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