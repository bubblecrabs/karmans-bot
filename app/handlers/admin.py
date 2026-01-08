from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.filters.admin import AdminFilter
from app.utils.keyboards import admin_kb

router = Router()


@router.callback_query(F.data == "admin", AdminFilter())
async def admin_callback(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="⬇️ <b>What do you want to do?</b>",
        reply_markup=admin_kb(),
    )
    await call.answer()
