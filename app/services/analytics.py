from app.core.config import settings


class Analytics:
    GA4_ENDPOINT = "https://www.google-analytics.com/mp/collect"

    def __init__(self) -> None:
        self.measurement_id: str = settings.GA4_MEASUREMENT_ID
        self.api_secret: str = settings.GA4_API_SECRET


analytics_service = Analytics()
