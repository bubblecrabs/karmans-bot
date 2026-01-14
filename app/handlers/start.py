from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart

from app.middlewares.subscription import SubscriptionMiddleware
from app.models.user import User
from app.utils.keyboards import start_kb

router = Router()
router.message.middleware(SubscriptionMiddleware())


@router.message(CommandStart())
async def start_command(message: Message, user: User) -> None:
    if not message.from_user:
        return

    await message.answer(
        text="✋ <b>Hi</b>",
        reply_markup=start_kb(is_superuser=user.is_superuser),
    )


@router.callback_query(F.data == "start")
async def start_callback(call: CallbackQuery, user: User) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="✋ <b>Hi</b>",
        reply_markup=start_kb(is_superuser=user.is_superuser),
    )
    await call.answer()


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    if call.message:
        await call.message.delete()

    await call.answer()
