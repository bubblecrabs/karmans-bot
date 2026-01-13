from enum import Enum as PyEnum


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
