from aiogram import Router

from app.handlers.start import router as start_router


def get_routers() -> Router:
    router = Router()
    router.include_router(router=start_router)
    return router
