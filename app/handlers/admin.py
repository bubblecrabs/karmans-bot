from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import AdminFilter
from app.services.admin import AdminService
from app.utils.keyboards import admin_kb, back_button_kb
from app.utils.messages import MENU_MESSAGE_KEY, STATS_MESSAGE_KEY

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
