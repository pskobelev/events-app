import logging

from aiogram.client.session import aiohttp

from api.api_routes import ApiRoutes
from utils import handle_response

logger = logging.getLogger(__name__)


async def api_add_event(params):
    url = ApiRoutes.get_full_url(ApiRoutes.ADD_EVENT)
    logger.info("Send req to: %s. With params: %s", url, params)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=params) as resp:
                logger.info(f"Start new game response: {resp}")
                try:
                    data = await handle_response(resp)
                    return data
                except ValueError as e:
                    logger.error("Catch exception: %s", e)
        except Exception as e:
            logger.exception("Get exception, %s", e)


async def api_write_user_choice(params):
    url = ApiRoutes.get_full_url(ApiRoutes.USER_CHOICE)
    logger.info("Writing user choice: %s", url)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params) as resp:
            data = await handle_response(resp)
            return data


async def api_get_event_stats(event_id: int):
    url = ApiRoutes.get_full_url(ApiRoutes.STATS, event_id=event_id)
    logger.debug("Get event stats. url: %s, event: %s", url, event_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await handle_response(resp)
            return data


async def api_close_active_event(chat_id):
    url = ApiRoutes.get_full_url(ApiRoutes.CLOSE_EVENT, chat_id=chat_id)
    logger.debug("Call url: %s", url)
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as resp:
            result = await handle_response(resp)
            return result
