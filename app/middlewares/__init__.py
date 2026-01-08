from aiogram import Dispatcher

from app.middlewares.auth import AuthMiddleware
from app.middlewares.locale import CustomI18nMiddleware
from app.middlewares.session import SessionMakerMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(SessionMakerMiddleware())

    dp.update.middleware(CustomI18nMiddleware())
    dp.update.middleware(AuthMiddleware())
