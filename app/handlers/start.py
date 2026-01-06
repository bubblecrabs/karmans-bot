from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.authorization import AuthService
from app.utils.keyboards import start_kb
from app.utils.messages import START_MESSAGE_KEY

router = Router()


@router.message(CommandStart())
async def start_command_handler(message: Message, session: AsyncSession) -> None:
    if not message.from_user:
        return

    user: User = await AuthService(session).authorization(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        is_premium=message.from_user.is_premium,
        language_code=message.from_user.language_code,
    )

    await message.answer(
        text=START_MESSAGE_KEY,
        reply_markup=start_kb(is_superuser=user.is_superuser),
    )


@router.callback_query(F.data == "start")
async def start_callback_handler(call: CallbackQuery, session: AsyncSession) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    user: User = await AuthService(session).authorization(
        user_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_premium=call.from_user.is_premium,
        language_code=call.from_user.language_code,
    )

    await call.message.edit_text(
        text=START_MESSAGE_KEY,
        reply_markup=start_kb(is_superuser=user.is_superuser),
    )
    await call.answer()
