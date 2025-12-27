from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth import AuthService
from app.utils.keyboards import start_kb
from app.utils.messages import start_message

router = Router()


@router.message(CommandStart())
async def start_command_handler(message: Message, session: AsyncSession) -> None:
    if not message.from_user:
        return

    auth_service = AuthService(session)

    await auth_service.authorization(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        is_premium=message.from_user.is_premium,
    )

    await message.answer(
        text=start_message,
        reply_markup=start_kb(),
    )


@router.callback_query(F.data == "start")
async def start_callback_handler(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text=start_message,
        reply_markup=start_kb(),
    )
    await call.answer()
