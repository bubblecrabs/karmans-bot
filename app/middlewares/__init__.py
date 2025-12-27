from aiogram import Dispatcher

from app.middlewares.analytics import AnalyticsMiddleware
from app.middlewares.session import DatabaseMiddleware


def get_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(DatabaseMiddleware())

    dp.update.middleware(AnalyticsMiddleware())
