from aiogram import Dispatcher

from app.core.bot import i18n
from app.middlewares.locale import CustomI18nMiddleware
from app.middlewares.posthog import PostHogMiddleware
from app.middlewares.session import SessionMakerMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(SessionMakerMiddleware())

    dp.update.middleware(CustomI18nMiddleware(i18n=i18n))
    dp.update.middleware(PostHogMiddleware())
