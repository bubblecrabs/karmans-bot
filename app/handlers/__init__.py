from aiogram import Router, Dispatcher

from app.handlers.start import router as start_router
from app.handlers.menu import router as menu_router
from app.handlers.lang import router as lang_router
from app.handlers.lang import router as help_router


def get_routers() -> Router:
    router = Router()
    router.include_router(router=start_router)
    router.include_router(router=menu_router)
    router.include_router(router=lang_router)
    router.include_router(router=help_router)
    return router


def setup_routers(dp: Dispatcher) -> None:
    dp.include_routers(get_routers())
