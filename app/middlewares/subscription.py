from collections.abc import Awaitable, Callable, Sequence
from typing import Any

from aiogram import BaseMiddleware, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import TelegramObject, User as TelegramUser, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.channel import Channel
from app.repositories.channels import ChannelRepository


class SubscriptionMiddleware(BaseMiddleware):
    """Middleware for verifying user subscriptions to channels"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        bot: Bot = data["bot"]
        session: AsyncSession = data["session"]
        telegram_user: TelegramUser | None = data.get("event_from_user")
        if not telegram_user:
            return await handler(event, data)

        channel_repo = ChannelRepository(session)
        active_channels: Sequence[Channel] = await channel_repo.get_active_channels()

        if not active_channels:
            return await handler(event, data)

        unsubscribed_channels: list[Channel] = []

        for channel in active_channels:
            try:
                member = await bot.get_chat_member(
                    chat_id=channel.channel_id,
                    user_id=telegram_user.id,
                )
                if member.status not in [
                    ChatMemberStatus.MEMBER,
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.CREATOR,
                ]:
                    unsubscribed_channels.append(channel)
            except Exception:
                continue

        if unsubscribed_channels:
            text = "🔒 <b>To use the bot, you need to subscribe to the channels:</b>\n\n"
            builder = InlineKeyboardBuilder()
            for ch in unsubscribed_channels:
                if ch.username:
                    text += f"• @{ch.username}\n"
                    builder.button(text=f"📢 {ch.title}", url=f"https://t.me/{ch.username}")
                elif ch.invite_link:
                    text += f"• {ch.title} (Private)\n"
                    builder.button(text=f"🔐 {ch.title}", url=ch.invite_link)
                else:
                    text += f"• {ch.title} (Contact the administrator)\n"

            builder.adjust(1)
            builder.button(text="✅ Check subscription", callback_data="check_subscription")

            if isinstance(event, Message):
                await event.answer(text=text, reply_markup=builder.as_markup())

            return

        return await handler(event, data)
