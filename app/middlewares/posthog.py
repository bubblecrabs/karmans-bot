from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, Message, CallbackQuery, ErrorEvent

from app.services.posthog import PostHogService


class PostHogMiddleware(BaseMiddleware):
    """Middleware for sending events to PostHog"""

    def __init__(self) -> None:
        super().__init__()
        self.posthog = PostHogService()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Update):
            if event.message:
                await self._track_message(message=event.message)

            if event.callback_query:
                await self._track_callback(callback=event.callback_query)

        if isinstance(event, ErrorEvent):
            await self._track_error(error_event=event)

        return await handler(event, data)

    async def _track_message(self, message: Message) -> None:
        if not message.from_user:
            return

        properties: dict[str, Any] = {
            "chat_id": message.chat.id,
            "message_id": message.message_id,
        }

        if message.text:
            properties["type"] = "text"
            properties["text"] = message.text
        elif message.photo:
            properties["type"] = "photo"
            properties["photo_count"] = len(message.photo)
        elif message.video:
            properties["type"] = "video"
            properties["video_duration"] = message.video.duration
        elif message.document:
            properties["type"] = "document"
            properties["file_name"] = message.document.file_name
        elif message.voice:
            properties["type"] = "voice"
            properties["voice_duration"] = message.voice.duration
        elif message.audio:
            properties["type"] = "audio"
            properties["audio_duration"] = message.audio.duration
        elif message.sticker:
            properties["type"] = "sticker"
            properties["sticker_emoji"] = message.sticker.emoji
        else:
            properties["type"] = "other"

        await self.posthog.track_event(
            user_id=message.from_user.id,
            event_name="message_received",
            properties=properties,
        )

    async def _track_callback(self, callback: CallbackQuery) -> None:
        if not callback.from_user:
            return

        properties: dict[str, Any] = {
            "callback_data": callback.data,
            "message_id": callback.message.message_id if callback.message else None,
        }

        await self.posthog.track_event(
            user_id=callback.from_user.id,
            event_name="button_clicked",
            properties=properties,
        )

    async def _track_error(self, error_event: ErrorEvent) -> None:
        update: Update = error_event.update
        exception: Exception = error_event.exception

        user_id: int | None = None

        if update.message and update.message.from_user:
            user_id: int = update.message.from_user.id
        elif update.callback_query and update.callback_query.from_user:
            user_id: int = update.callback_query.from_user.id

        if not user_id:
            return

        properties: dict[str, Any] = {
            "error_type": type(exception).__name__,
            "error_message": str(object=exception),
            "update_type": update.event_type if hasattr(update, "event_type") else "unknown",
        }

        await self.posthog.track_error(
            user_id=user_id,
            error=exception,
            context=properties,
        )
