from aiogram import Dispatcher

from app.middlewares.session import SessionMakerMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(SessionMakerMiddleware())
