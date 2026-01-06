from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TGUser, Message, CallbackQuery

from app.core.redis import redis_cache
from app.models.user import User
from app.repositories.users import UserRepository
from app.utils.messages import BANNED_MESSAGE_KEY


class BanCheckMiddleware(BaseMiddleware):
    """Middleware for checking user blocking"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: TGUser | None = data.get("event_from_user")

        if not user:
            return await handler(event, data)

        session: Any | None = data.get("session")
        if not session:
            return await handler(event, data)

        repository = UserRepository(session)

        user_data: User | None = await repository.get_user_by_user_id(user_id=user.id)
        if user_data and user_data.is_superuser:
            return await handler(event, data)

        if await repository.is_user_banned(user_id=user.id):
            await self._handle_banned_user(user_id=user.id, event=event)
            return None

        return await handler(event, data)

    async def _handle_banned_user(self, user_id: int, event: TelegramObject) -> None:
        cache_key = f"ban_notified:{user_id}"

        if not await redis_cache.exists(cache_key):
            if isinstance(event, Message):
                await event.answer(text=BANNED_MESSAGE_KEY)
            elif isinstance(event, CallbackQuery):
                await event.answer(text="You are blocked", show_alert=True)

            await redis_cache.set(key=cache_key, value=True, ttl=300)
        else:
            if isinstance(event, CallbackQuery):
                await event.answer()
