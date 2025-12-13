__all__ = ("router",)

from aiogram import Router

router = Router(name=__name__)

from routers.calendar_handler import router as calendar_router
from routers.common import router as common_router

router.include_routers(
    calendar_router,
    common_router,
)
