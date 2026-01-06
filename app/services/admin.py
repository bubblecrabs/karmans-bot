from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.users import UserRepository


class AdminService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repository: UserRepository = UserRepository(session)
        self.session: AsyncSession = session

    async def statistics(self) -> dict:
        users_count: int = await self.user_repository.count_users()
        last_user: User | None = await self.user_repository.get_last_joined_user()

        return {
            "total_users": users_count,
            "last_user": self._format_user(user=last_user),
            "joined_at": self._format_datetime(dt=last_user.created_at if last_user else None),
        }

    @staticmethod
    def _format_user(user: User | None) -> str:
        if not user:
            return "—"
        return f"@{user.username}" if user.username else f"ID: {user.user_id}"

    @staticmethod
    def _format_datetime(dt: datetime | None) -> str:
        return dt.strftime(format="%d.%m.%Y %H:%M") if dt else "—"
