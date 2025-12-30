from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.authorization import AuthService
from app.utils.keyboards import lang_kb
from app.utils.messages import LANG_MESSAGE_KEY, SET_LANG_MESSAGE_KEY

router = Router()


@router.message(Command("lang"))
async def lang_command_handler(message: Message) -> None:
    if not message.from_user:
        return

    await message.answer(
        text=_(LANG_MESSAGE_KEY),
        reply_markup=lang_kb(),
    )


@router.callback_query(F.data.startswith("lang_"))
async def lang_callback_handler(call: CallbackQuery, session: AsyncSession) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    if not call.data:
        await call.answer()
        return

    language_code: str = call.data.split(sep="_")[1].lower()

    auth_service = AuthService(session)

    await auth_service.authorization(
        user_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_premium=call.from_user.is_premium,
        language_code=language_code,
    )

    await call.message.edit_text(
        text=_(SET_LANG_MESSAGE_KEY),
    )
    await call.answer()
