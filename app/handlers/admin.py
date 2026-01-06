from typing import Any

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import AdminFilter
from app.services.admin import AdminService
from app.utils.keyboards import admin_kb, manage_users_kb, back_button_kb
from app.utils.messages import (
    MENU_MESSAGE_KEY,
    STATS_MESSAGE_KEY,
    MANAGE_USERS_MESSAGE_KEY,
    WRONG_ID_MESSAGE_KEY,
    USER_BLOCKED_SUCCESS_KEY,
    USER_UNBLOCKED_SUCCESS_KEY,
    USER_NOT_FOUND_KEY,
    UNKNOWN_OPERATION_KEY,
)
from app.utils.states import AdminStates

router = Router()


@router.callback_query(F.data == "admin", AdminFilter())
async def admin_callback_handler(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text=MENU_MESSAGE_KEY,
        reply_markup=admin_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "stats", AdminFilter())
async def stats_callback_handler(call: CallbackQuery, session: AsyncSession) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    stats: dict = await AdminService(session=session).statistics()

    await call.message.edit_text(
        text=STATS_MESSAGE_KEY.format(**stats),
        reply_markup=back_button_kb(callback_data="admin"),
    )
    await call.answer()


@router.callback_query(F.data == "manage_users", AdminFilter())
async def manage_users_callback_handler(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text=MENU_MESSAGE_KEY,
        reply_markup=manage_users_kb(),
    )
    await call.answer()


@router.callback_query(F.data.in_(iterable=["block_user", "unblock_user"]), AdminFilter())
async def get_user_id_callback_handler(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await state.update_data(func=call.data)

    await call.message.edit_text(
        text=MANAGE_USERS_MESSAGE_KEY,
        reply_markup=back_button_kb(callback_data="manage_users"),
    )
    await call.answer()
    await state.set_state(state=AdminStates.id)


@router.message(StateFilter(AdminStates.id), AdminFilter())
async def update_user_message_handler(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if not message.from_user:
        return

    if not message.text or not message.text.isdigit():
        await message.answer(text=WRONG_ID_MESSAGE_KEY)
        return

    data: dict[str, Any] = await state.get_data()
    user_id = int(message.text)
    func: Any | None = data.get("func")

    admin_service = AdminService(session)

    if func == "block_user":
        success: bool = await admin_service.block_user(user_id=user_id)
        text: str = (
            USER_BLOCKED_SUCCESS_KEY.format(user_id=user_id)
            if success
            else USER_NOT_FOUND_KEY.format(user_id=user_id)
        )
    elif func == "unblock_user":
        success: bool = await admin_service.unblock_user(user_id=user_id)
        text: str = (
            USER_UNBLOCKED_SUCCESS_KEY.format(user_id=user_id)
            if success
            else USER_NOT_FOUND_KEY.format(user_id=user_id)
        )
    else:
        text: str = UNKNOWN_OPERATION_KEY

    await message.answer(
        text=text,
        reply_markup=back_button_kb(callback_data="manage_users"),
    )
    await state.clear()
