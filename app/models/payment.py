from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String, Numeric, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class PaymentCurrency(str, PyEnum):
    USD = "USD"
    XTR = "XTR"


class PaymentStatus(str, PyEnum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELED = "canceled"


class PaymentProvider(str, PyEnum):
    TELEGRAM_STARS = "telegram_stars"
    CRYPTO = "crypto"


class Payment(Base):
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(column="users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    charge_id: Mapped[str | None] = mapped_column(
        String(length=255),
        nullable=True,
        unique=True,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric[Decimal](precision=10, scale=2),
        nullable=False,
    )
    currency: Mapped[PaymentCurrency] = mapped_column(
        Enum(PaymentCurrency, native_enum=False, length=3),
        nullable=False,
        default=PaymentCurrency.USD,
    )
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, native_enum=False, length=20),
        nullable=False,
        default=PaymentStatus.PENDING,
        index=True,
    )
    provider: Mapped[PaymentProvider] = mapped_column(
        Enum(PaymentProvider, native_enum=False, length=30),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        String(length=500),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Relationship
    user: Mapped["User"] = relationship(
        argument="User",
        back_populates="payments",
        lazy="selectin",
    )
