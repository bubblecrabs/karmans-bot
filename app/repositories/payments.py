from collections.abc import AsyncGenerator, Sequence
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select, delete, case, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment, PaymentCurrency, PaymentProvider, PaymentStatus


class PaymentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def create_payment(
        self,
        user_id: int,
        charge_id: str | None,
        amount: Decimal,
        currency: PaymentCurrency,
        status: PaymentStatus,
        provider: PaymentProvider,
        description: str | None = None,
    ) -> Payment:
        payment = Payment(
            user_id=user_id,
            charge_id=charge_id,
            amount=amount,
            currency=currency,
            status=status,
            provider=provider,
            description=description,
        )
        self.session.add(instance=payment)
        await self.session.flush()
        await self.session.refresh(instance=payment)
        return payment

    async def update_payment(
        self,
        payment: Payment,
        user_id: int,
        charge_id: str | None,
        amount: Decimal,
        currency: PaymentCurrency,
        status: PaymentStatus,
        provider: PaymentProvider,
        description: str | None = None,
    ) -> Payment:
        payment.user_id = user_id
        payment.charge_id = charge_id
        payment.amount = amount
        payment.currency = currency
        payment.status = status
        payment.provider = provider
        payment.description = description

        await self.session.flush()
        await self.session.refresh(instance=payment)
        return payment

    async def delete_payment(self, payment_id: UUID) -> bool:
        stmt = delete(table=Payment).where(Payment.id == payment_id)
        result = await self.session.execute(statement=stmt)
        return getattr(result, "rowcount", 0) > 0

    async def get_payment_by_id(self, payment_id: UUID) -> Payment | None:
        stmt = select(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_payments(self, batch_size: int = 1000) -> AsyncGenerator[Payment | None]:
        stmt = select(Payment).execution_options(yield_per=batch_size, stream_results=True)
        stream = await self.session.stream_scalars(statement=stmt)

        async for payment in stream:
            yield payment

    async def get_payments_by_user_id(self, user_id: int) -> Sequence[Payment]:
        stmt = select(Payment).where(Payment.user_id == user_id)
        result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_payment_stats(
        self,
        currency: PaymentCurrency = PaymentCurrency.USD,
    ) -> dict[str, int | Decimal]:
        today_start: datetime = datetime.combine(date=date.today(), time=datetime.min.time())

        count_stmt = select(
            func.count(Payment.id).label("total"),
            func.count(case((Payment.created_at >= today_start, 1))).label("today"),
        ).where(Payment.currency == currency)

        count_result = await self.session.execute(statement=count_stmt)
        counts = count_result.one()

        revenue_stmt = select(
            func.sum(Payment.amount).label("total"),
            func.sum(case((Payment.created_at >= today_start, Payment.amount))).label("today"),
        ).where(Payment.currency == currency, Payment.status == PaymentStatus.PAID)

        revenue_result = await self.session.execute(statement=revenue_stmt)
        revenue = revenue_result.one()

        return {
            "total_payments": counts.total,
            "payments_today": counts.today,
            "total_revenue": Decimal(value=str(object=revenue.total or 0)),
            "revenue_today": Decimal(value=str(object=revenue.today or 0)),
        }
