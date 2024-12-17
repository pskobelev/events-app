from aiogram.client.session import aiohttp
from aiohttp import ClientSession

from api.users.schemas import UserBase

from .utils import handle_response
from core.config import get_config
from core.utils import configure_logging

cfg = get_config()
logger = configure_logging()

URL = f"{cfg.API_PATH}"


async def api_register_user(user_in: UserBase):
    url = URL + "/users/"
    payload = user_in.model_dump()
    logger.debug("URL is: %s. Payload is %s", url, payload)

    async with ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            resp.raise_for_status()
            logger.debug("Get response: %s, status: %s", resp.json(),
                         resp.status)
            return await resp.json()


async def api_add_new_event(chat_id, message):
    async with aiohttp.ClientSession() as session:
        try:
            logger.info("Start new game")
            async with session.post(
                    URL + "/events/add/",
                    json={"name": message.text, "chat_id": chat_id},
            ) as resp:
                logger.debug("Request: %s", resp)
                try:
                    data = await handle_response(resp)
                    logger.debug("=>> Handle data: %s", data)
                    await message.answer(f"Msg from database: {data}")
                except ValueError as e:
                    logger.error("Catch exception: %s", e)
        except Exception as e:
            logger.exception("Get exception, %s", e)
            await message.reply(f"Unexpected error. \n{e}")


async def is_active_game(chat_id):
    pass


async def start_new_game(chat_id, message):
    pass
