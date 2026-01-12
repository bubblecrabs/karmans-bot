from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.payment import PaymentCurrency, PaymentStatus, PaymentProvider
from app.repositories.users import UserRepository
from app.repositories.payments import PaymentRepository


class PaymentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session
        self.user_repo: UserRepository = UserRepository(session)
        self.payment_repo: PaymentRepository = PaymentRepository(session)

    async def process_successful_payment(
        self,
        user_id: int,
        charge_id: str,
        amount: int,
        currency: str,
        duration_days: int,
        description: str,
    ) -> bool:
        user: User | None = await self.user_repo.get_user_by_user_id(user_id=user_id)
        if not user:
            return False

        payment_currency: PaymentCurrency = (
            PaymentCurrency.XTR if currency == "XTR" else PaymentCurrency.USD
        )

        await self.payment_repo.create_payment(
            user_id=user_id,
            charge_id=charge_id,
            amount=Decimal(value=amount),
            currency=payment_currency,
            status=PaymentStatus.PAID,
            provider=PaymentProvider.TELEGRAM_STARS,
            description=description,
        )

        now: datetime = datetime.now(tz=timezone.utc)
        user.is_premium = True

        if user.premium_until and user.premium_until > now:
            user.premium_until = user.premium_until + timedelta(days=duration_days)
        else:
            user.premium_until = now + timedelta(days=duration_days)

        await self.session.flush()
        await self.session.refresh(instance=user)
        return True
