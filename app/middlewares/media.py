from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class MediaGroupMiddleware(BaseMiddleware):
    """Middleware for preventing duplicate processing of media group messages"""

    def __init__(self):
        self.processed_media_groups: set[str] = set[str]()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["processed_media_groups"] = self.processed_media_groups
        return await handler(event, data)
