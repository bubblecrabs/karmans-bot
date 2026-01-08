from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.utils.keyboards import menu_kb

router = Router()


@router.callback_query(F.data.startswith("button_"))
async def menu_callback(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="⬇️ <b>What do you want to do?</b>",
        reply_markup=menu_kb(),
    )
    await call.answer()
