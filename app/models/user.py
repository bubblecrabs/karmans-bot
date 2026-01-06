from datetime import datetime

from sqlalchemy import BigInteger, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(length=32), unique=True, nullable=True)
    first_name: Mapped[str] = mapped_column(String(length=64), unique=False, nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(length=64), unique=False, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_premium: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    language_code: Mapped[str | None] = mapped_column(String(length=10), unique=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
