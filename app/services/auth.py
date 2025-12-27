from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.users import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repository: UserRepository = UserRepository(session)
        self.session: AsyncSession = session

    async def authorization(
        self,
        user_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
        is_premium: bool | None,
    ) -> User:
        existing_user: User | None = await self.user_repository.get_user_by_user_id(user_id)

        if existing_user is None:
            user: User = await self.user_repository.create_user(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_premium=is_premium,
                is_superuser=False,
            )
        else:
            user: User = await self.user_repository.update_user(
                user=existing_user,
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_premium=is_premium,
            )

        await self.session.commit()
        return user
