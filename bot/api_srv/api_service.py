import logging

from aiogram.client.session import aiohttp
from app.api.api_routes import ApiRoutes
from utils.mods import handle_response

logger = logging.getLogger(__name__)


async def api_add_event(params):
    url = ApiRoutes.get_full_url(ApiRoutes.ADD_EVENT)
    logger.debug("Send req to: %s. With params: %s", url, params)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=params) as resp:
                logger.debug(f"Start new game response: {resp}")
                try:
                    data = await handle_response(resp)
                    return data
                except ValueError as e:
                    logger.error("Catch exception: %s", e)
        except Exception as e:
            logger.exception("Get exception, %s", e)


async def api_write_user_choice(params):
    """write user choice to database"""
    url = ApiRoutes.get_full_url(ApiRoutes.USER_CHOICE)
    logger.debug("Call ENDPOINT: %s. PARAMS: %s", url, params)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params) as resp:
            data = await handle_response(resp)
            return data


async def api_get_event_stats(event_id: int) -> dict:
    """return stat of current event"""
    url = ApiRoutes.get_full_url(ApiRoutes.STATS)
    params = {"event_id": event_id}
    logger.debug("Call ENDPOINT: %s. PARAMS: %s", url, params)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as resp:
                data = await handle_response(resp)
                return data
        except ValueError as e:
            raise ValueError from e


async def api_get_all_events():
    url = ApiRoutes.get_full_url(ApiRoutes.LIST_EVENT)
    logger.info("Get all events: %s", url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await handle_response(resp)
            return data


async def api_get_current_event(event_id: int, chat_id: int) -> list:
    url = ApiRoutes.get_full_url(ApiRoutes.FIND_EVENT)
    params = {"event_id": event_id, "chat_id": chat_id}
    logger.debug("Call ENDPOINT: %s. PARAMS: %s", url, params)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await handle_response(resp)
            if not data:
                logger.warning(
                    "Empty response for event_id=%s and chat_id=%s",
                    event_id,
                    chat_id,
                )
            return data


async def api_close_active_event(chat_id):
    url = ApiRoutes.get_full_url(ApiRoutes.CLOSE_EVENT)
    params = {"chat_id": chat_id}
    logger.debug("Call ENDPOINT: %s. PARAMS: %s", url, params)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as resp:
            result = await handle_response(resp)
            return result
