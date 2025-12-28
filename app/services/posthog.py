from datetime import datetime

import httpx

from app.core.config import settings


class PostHogService:
    def __init__(self) -> None:
        self.api_key: str = settings.POSTHOG_API_TOKEN
        self.base_url: str = settings.POSTHOG_BASE_URL
        self.headers: dict = {"Content-Type": "application/json"}
        self.client = httpx.AsyncClient(timeout=10.0)

    async def track_event(
        self,
        user_id: int,
        event_name: str,
        properties: dict,
    ) -> None:
        """
        Send an event to PostHog

        Args:
            user_id: User ID
            event: Event name
            properties: Additional data
        """
        payload: dict = {
            "api_key": self.api_key,
            "distinct_id": str(object=user_id),
            "event": event_name,
            "properties": properties or {},
            "timestamp": datetime.now().isoformat(),
        }

        try:
            response: httpx.Response = await self.client.post(
                url=f"{self.base_url}/i/v0/e/",
                json=payload,
            )
            response.raise_for_status()
        except Exception as e:
            print(f"PostHog tracking error: {e}")

    async def track_error(
        self,
        user_id: int,
        error: Exception,
        context: dict | None = None,
    ) -> None:
        """
        Send error to PostHog

        Args:
            user_id: User ID
            error: Exception
            context: Additional context
        """
        properties: dict = {
            "error_type": type(error).__name__,
            "error_message": str(object=error),
            **(context or {}),
        }
        await self.track_event(
            user_id=user_id,
            event_name="bot_error",
            properties=properties,
        )

    async def close(self) -> None:
        await self.client.aclose()
