from typing import Any

from aiogram.types import TelegramObject, User
from aiogram.utils.i18n.middleware import I18nMiddleware


class CustomI18nMiddleware(I18nMiddleware):
    """Custom I18n middleware with language detection"""

    SUPPORTED_LANGUAGES: set[str] = {"ru", "uk", "en"}
    DEFAULT_LANGUAGE = "en"

    async def get_locale(self, event: TelegramObject, data: dict[str, Any]) -> str:
        """
        Detect current user locale based on event and context.

        Args:
            event: Telegram event object
            data: Context data

        Returns:
            Locale string (ru, uk, or en)
        """
        user: User | None = data.get("event_from_user")

        if not user or not user.language_code:
            return self.DEFAULT_LANGUAGE

        base_language: str = user.language_code.split(sep="-")[0].lower()

        if base_language in self.SUPPORTED_LANGUAGES:
            return base_language

        return self.DEFAULT_LANGUAGE
