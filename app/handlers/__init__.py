from aiogram import Router, Dispatcher

from app.handlers.start import router as start_router
from app.handlers.menu import router as menu_router
from app.handlers.help import router as help_router
from app.handlers.admin import router as admin_router
from app.handlers.stats import router as stats_router
from app.handlers.mailing import router as mailing_router
from app.handlers.moderation import router as moderation_router
from app.handlers.payments import router as payments_router


def get_routers() -> Router:
    router = Router()
    router.include_router(router=start_router)
    router.include_router(router=menu_router)
    router.include_router(router=help_router)
    router.include_router(router=admin_router)
    router.include_router(router=stats_router)
    router.include_router(router=mailing_router)
    router.include_router(router=moderation_router)
    router.include_router(router=payments_router)
    return router


def setup_routers(dp: Dispatcher) -> None:
    dp.include_routers(get_routers())
