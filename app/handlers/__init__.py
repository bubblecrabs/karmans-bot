from aiogram import Router

from app.handlers.start import router as start_router
from app.handlers.menu import router as menu_router
from app.handlers.language import router as lang_router


def get_routers() -> Router:
    router = Router()
    router.include_router(router=start_router)
    router.include_router(router=menu_router)
    router.include_router(router=lang_router)
    return router
