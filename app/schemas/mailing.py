from datetime import datetime

from pydantic import BaseModel


class MailingMessage(BaseModel):
    text: str
    image: str | None = None
    button_text: str | None = None
    button_url: str | None = None
    scheduled_time: datetime | None = None
