from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import AdminFilter
from app.services.admin import AdminService
from app.utils.keyboards import moderation_kb, back_button_kb
from app.utils.states import AdminStates

router = Router()


@router.callback_query(F.data == "moderation", AdminFilter())
async def moderation_callback(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="⬇️ <b>What do you want to do?</b>",
        reply_markup=moderation_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "ban_user_id", AdminFilter())
async def moderation_ban_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="➡️ <b>Enter the Telegram user ID:</b>",
        reply_markup=back_button_kb(callback_data="moderation"),
    )
    await state.set_state(state=AdminStates.ban_user_id)
    await call.answer()


@router.callback_query(F.data == "unban_user_id", AdminFilter())
async def moderation_unban_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="➡️ <b>Enter the Telegram user ID:</b>",
        reply_markup=back_button_kb(callback_data="moderation"),
    )
    await state.set_state(state=AdminStates.unban_user_id)
    await call.answer()


@router.message(StateFilter(AdminStates.ban_user_id), AdminFilter())
async def moderation_ban_message(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if not message.from_user or not message.text:
        return

    if not message.text.isdigit():
        await message.answer(text="⁉️ <b>Incorrect Telegram user ID.</b>")
        return

    user_id = int(message.text)

    if user_id == message.from_user.id:
        await message.answer(text="❌ <b>You cannot block yourself.</b>")
        return

    success: bool = await AdminService(session).block_user(user_id=user_id)

    text: str = (
        f"✅ <b>User {user_id} has been blocked.</b>"
        if success
        else f"❌ <b>User {user_id} not found.</b>"
    )

    await message.answer(
        text=text,
        reply_markup=back_button_kb(callback_data="moderation"),
    )
    await state.clear()


@router.message(StateFilter(AdminStates.unban_user_id), AdminFilter())
async def moderation_unban_message(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if not message.from_user or not message.text:
        return

    if not message.text.isdigit():
        await message.answer(text="⁉️ <b>Incorrect Telegram user ID.</b>")
        return

    user_id = int(message.text)
    success: bool = await AdminService(session).unblock_user(user_id=user_id)

    text: str = (
        f"✅ <b>User {user_id} has been unblocked.</b>"
        if success
        else f"❌ <b>User {user_id} not found.</b>"
    )

    await message.answer(
        text=text,
        reply_markup=back_button_kb(callback_data="moderation"),
    )
    await state.clear()
