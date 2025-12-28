from aiogram import Dispatcher

from app.middlewares.posthog import PostHogMiddleware
from app.middlewares.session import SessionMakerMiddleware


def get_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(SessionMakerMiddleware())

    dp.update.middleware(PostHogMiddleware())
