import asyncio
import logging

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.users import UserRepository

logger: logging.Logger = logging.getLogger(name=__name__)


class MailingService:
    def __init__(self, session: AsyncSession, bot: Bot):
        self.session: AsyncSession = session
        self.repository = UserRepository(session)
        self.bot: Bot = bot

    async def send_mailing(
        self,
        text: str,
        image: str | None = None,
        button_text: str | None = None,
        button_url: str | None = None,
    ) -> dict[str, int]:
        stats: dict[str, int] = {
            "total": 0,
            "success": 0,
            "blocked": 0,
            "failed": 0,
        }

        reply_markup: InlineKeyboardMarkup | None = self._build_keyboard(button_text, button_url)

        blocked_user_ids: list[int] = []

        async for user in self.repository.get_users():
            if not user:
                continue

            stats["total"] += 1

            try:
                await self._send_to_user(
                    user_id=user.user_id,
                    text=text,
                    image=image,
                    reply_markup=reply_markup,
                )
                stats["success"] += 1

            except TelegramForbiddenError:
                stats["blocked"] += 1
                blocked_user_ids.append(user.user_id)

            except (TelegramBadRequest, Exception) as e:
                stats["failed"] += 1
                logger.error(msg=f"Error sending to {user.user_id}: {e}")

            await asyncio.sleep(delay=0.05)

        if blocked_user_ids:
            await self.repository.set_users_inactive(blocked_user_ids)
            await self.session.commit()

        return stats

    async def _send_to_user(
        self,
        user_id: int,
        text: str,
        image: str | None,
        reply_markup: InlineKeyboardMarkup | None,
    ) -> None:
        if image:
            await self.bot.send_photo(
                chat_id=user_id,
                photo=image,
                caption=text,
                reply_markup=reply_markup,
            )
        else:
            await self.bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=reply_markup,
            )

    @staticmethod
    def _build_keyboard(
        button_text: str | None,
        button_url: str | None,
    ) -> InlineKeyboardMarkup | None:
        if button_text and button_url:
            return InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=button_text, url=button_url)]]
            )
        return None
