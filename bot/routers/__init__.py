__all__ = ("router",)

from aiogram import Router

router = Router(name=__name__)

from .calendar_handler import router as calendar_router  # noqa: E402
from .common import router as common_router  # noqa: E402

router.include_routers(
    calendar_router,
    common_router,
)

# this one is LAST
