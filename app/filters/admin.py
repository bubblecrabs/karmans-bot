from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.users import UserRepository


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        if not message.from_user:
            return False

        repository = UserRepository(session=session)

        user: User | None = await repository.get_user_by_user_id(user_id=message.from_user.id)
        if not user:
            return False

        return user.is_superuser
