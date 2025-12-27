from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.utils.keyboards import menu_kb
from app.utils.messages import menu_message

router = Router()


@router.callback_query(F.data.startswith("button_"))
async def start_callback_handler(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text=menu_message,
        reply_markup=menu_kb(),
    )
    await call.answer()
