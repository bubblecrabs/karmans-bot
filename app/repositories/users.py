from collections.abc import AsyncGenerator, Sequence
from datetime import datetime, date

from sqlalchemy import select, delete, update, case, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def create_user(
        self,
        user_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
        is_telegram_premium: bool,
        is_premium: bool,
        is_superuser: bool,
        is_active: bool,
        is_banned: bool,
        language_code: str | None,
        premium_until: datetime | None,
    ) -> User:
        user = User(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_telegram_premium=is_telegram_premium,
            is_premium=is_premium,
            is_superuser=is_superuser,
            is_active=is_active,
            is_banned=is_banned,
            language_code=language_code,
            premium_until=premium_until,
        )
        self.session.add(instance=user)
        await self.session.flush()
        await self.session.refresh(instance=user)
        return user

    async def update_user(
        self,
        user: User,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        is_telegram_premium: bool | None = None,
        is_premium: bool | None = None,
        is_active: bool | None = None,
        is_banned: bool | None = None,
        language_code: str | None = None,
        premium_until: datetime | None = None,
    ) -> User:
        if username is not None:
            user.username = username
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if is_telegram_premium is not None:
            user.is_telegram_premium = is_telegram_premium
        if is_premium is not None:
            user.is_premium = is_premium
        if is_active is not None:
            user.is_active = is_active
        if is_banned is not None:
            user.is_banned = is_banned
        if language_code is not None:
            user.language_code = language_code
        if premium_until is not None:
            user.premium_until = premium_until

        await self.session.flush()
        await self.session.refresh(instance=user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        stmt = delete(table=User).where(User.user_id == user_id)
        result = await self.session.execute(statement=stmt)
        return getattr(result, "rowcount", 0) > 0

    async def get_user_by_user_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.user_id == user_id)
        result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_all_users(self, batch_size: int = 1000) -> AsyncGenerator[User | None]:
        stmt = select(User).execution_options(
            yield_per=batch_size,
            stream_results=True,
        )
        stream = await self.session.stream_scalars(statement=stmt)

        async for user in stream:
            yield user

    async def get_active_users(self) -> Sequence[User]:
        stmt = select(User).where(User.is_active == True)  # noqa: E712
        result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_active_user_ids(self) -> Sequence[int]:
        stmt = select(User.user_id).where(User.is_active == True)  # noqa: E712
        result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def set_user_active(self, user_id: int, is_active: bool) -> User | None:
        stmt = (
            update(table=User)
            .where(User.user_id == user_id)
            .values(is_active=is_active)
            .returning(User)
        )
        result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def set_users_inactive(self, user_ids: list[int]) -> Sequence[int]:
        stmt = (
            update(table=User)
            .where(User.user_id.in_(other=user_ids))
            .values(is_active=False)
            .returning(User.user_id)
        )
        result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_user_stats(self) -> dict[str, int]:
        today_start: datetime = datetime.combine(date=date.today(), time=datetime.min.time())

        stmt = select(
            func.count(User.user_id).label("total_users"),
            func.count(case((User.created_at >= today_start, 1))).label("new_today"),
            func.count(case((User.is_active == True, 1))).label("active_users"),  # noqa: E712
            func.count(case((User.is_banned == True, 1))).label("banned_users"),  # noqa: E712
        )

        result = await self.session.execute(statement=stmt)
        row = result.one()

        return {
            "total_users": row.total_users,
            "new_users_today": row.new_today,
            "active_users": row.active_users,
            "banned_users": row.banned_users,
        }
