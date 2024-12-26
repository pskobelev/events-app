import logging

from aiogram.client.session import aiohttp

from core.config import settings
from utils import handle_response

logger = logging.getLogger(__name__)

URL = f"{settings.api.prefix}{settings.api.host}:{settings.api.port}"


async def api_add_new_event(params):
    async with aiohttp.ClientSession() as session:
        try:
            logger.info("Start new game")
            async with session.post(
                    URL + "/events/add/",
                    json=params,
            ) as resp:
                logger.debug("Send request: %s", resp.url)
                try:
                    data = await handle_response(resp)
                    return data
                except ValueError as e:
                    logger.error("Catch exception: %s", e)
        except Exception as e:
            logger.exception("Get exception, %s", e)


# region TODO: write fucking code
async def is_active_game(chat_id):
    pass


async def start_new_game(chat_id, message):
    pass
# endregion
