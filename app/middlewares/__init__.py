from aiogram import Dispatcher

from app.middlewares.banned import BanCheckMiddleware
from app.middlewares.session import SessionMakerMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(SessionMakerMiddleware())

    dp.message.middleware(BanCheckMiddleware())
    dp.callback_query.middleware(BanCheckMiddleware())
