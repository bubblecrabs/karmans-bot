from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.users import UserRepository


class AuthMiddleware(BaseMiddleware):
    """Middleware for automatic user authorization"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        telegram_user: TelegramUser | None = data.get("event_from_user")

        if not telegram_user:
            return await handler(event, data)

        session: AsyncSession = data["session"]
        user_repo = UserRepository(session)

        user: User | None = await user_repo.get_user_by_user_id(user_id=telegram_user.id)

        if user is None:
            user = await user_repo.create_user(
                user_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
                is_telegram_premium=telegram_user.is_premium,
                is_premium=False,
                is_superuser=False,
                is_active=True,
                is_banned=False,
                language_code=telegram_user.language_code,
                premium_until=None,
            )

        if user.is_banned:
            return

        data["user"] = user

        return await handler(event, data)
