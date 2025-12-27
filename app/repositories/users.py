from collections.abc import AsyncGenerator

from sqlalchemy import select, delete
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
        is_premium: bool | None,
        is_superuser: bool = False,
    ) -> User:
        user = User(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_premium=is_premium,
            is_superuser=is_superuser,
        )
        self.session.add(instance=user)
        await self.session.flush()
        await self.session.refresh(instance=user)
        return user

    async def update_user(
        self,
        user: User,
        username: str | None,
        first_name: str,
        last_name: str | None,
        is_premium: bool | None,
    ) -> User:
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.is_premium = is_premium

        await self.session.flush()
        await self.session.refresh(instance=user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        stmt = delete(table=User).where(User.user_id == user_id)
        result = await self.session.execute(statement=stmt)
        await self.session.flush()

        rowcount = getattr(result, "rowcount", 0)
        return rowcount > 0

    async def get_user_by_user_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.user_id == user_id)
        result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_users(self, batch_size: int = 1000) -> AsyncGenerator[User | None]:
        stmt = select(User).execution_options(yield_per=batch_size, stream_results=True)
        stream = await self.session.stream_scalars(statement=stmt)

        async for user in stream:
            yield user
