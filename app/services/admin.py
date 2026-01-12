from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.users import UserRepository
from app.repositories.payments import PaymentRepository


class AdminService:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session
        self.user_repo: UserRepository = UserRepository(session)
        self.payment_repo: PaymentRepository = PaymentRepository(session)

    async def statistics(self) -> dict:
        user_stats: dict[str, int] = await self.user_repo.get_user_stats()
        payment_stats: dict[str, int | Decimal] = await self.payment_repo.get_payment_stats()

        return {
            **user_stats,
            **payment_stats,
        }

    async def block_user(self, user_id: int) -> bool:
        user: User | None = await self.user_repo.get_user_by_user_id(user_id=user_id)
        if not user:
            return False

        user.is_banned = True
        return True

    async def unblock_user(self, user_id: int) -> bool:
        user: User | None = await self.user_repo.get_user_by_user_id(user_id=user_id)
        if not user:
            return False

        user.is_banned = False
        return True

    async def add_premium(self, user_id: int, days: int) -> bool:
        user: User | None = await self.user_repo.get_user_by_user_id(user_id=user_id)
        if not user:
            return False

        user.is_premium = True

        now: datetime = datetime.now(tz=timezone.utc)
        if user.premium_until and user.premium_until > now:
            user.premium_until = user.premium_until + timedelta(days=days)
        else:
            user.premium_until = now + timedelta(days=days)
        return True
