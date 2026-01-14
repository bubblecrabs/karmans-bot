from collections.abc import Sequence
from typing import Any

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup

from app.core.nats import broker
from app.schemas.mailing import MailingMessage
from app.utils.keyboards import url_button_kb


class MailingService:
    """Service for handling mailing operations through NATS message queue"""

    SUBJECT_IMMEDIATE = "mailing.immediate"
    SUBJECT_SCHEDULED = "mailing.scheduled"

    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    async def send_immediate_mailing(self, message_data: MailingMessage) -> None:
        await broker.publish(
            message=message_data.model_dump(),
            subject=self.SUBJECT_IMMEDIATE,
        )

    async def send_scheduled_mailing(self, message_data: MailingMessage) -> None:
        if not message_data.scheduled_time:
            raise ValueError("scheduled_time is required for scheduled mailing")

        await broker.publish(
            message=message_data.model_dump(),
            subject=self.SUBJECT_SCHEDULED,
        )

    async def process_mailing(
        self,
        message_data: dict[str, Any],
        user_ids: Sequence[int],
    ) -> dict[str, int]:
        text: str = message_data["text"]
        image: str | None = message_data.get("image")
        button_text: str | None = message_data.get("button_text")
        button_url: str | None = message_data.get("button_url")

        if button_text and button_url:
            reply_markup: InlineKeyboardMarkup = url_button_kb(
                text=button_text,
                url=button_url,
            )

        success_count = 0
        failed_count = 0

        for user_id in user_ids:
            try:
                await self._send_to_user(
                    user_id=user_id,
                    text=text,
                    image=image,
                    reply_markup=reply_markup,
                )
                success_count += 1
            except Exception:
                failed_count += 1
                continue

        return {
            "success": success_count,
            "failed": failed_count,
        }

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
