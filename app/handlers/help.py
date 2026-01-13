from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.utils.keyboards import back_button_kb

router = Router()


@router.callback_query(F.data == "help")
async def help_callback(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text=(
            "ℹ️ <b>Help</b>\n\n"
            "🤖 <b>How to use the bot:</b>\n"
            "• Text\n"
            "• Text\n"
            "• Text\n\n"
            "📊 <b>Buttons:</b>\n"
            "• <b>Button 1</b> - Text\n"
            "• <b>Button 2</b> - Text\n"
            "• <b>Premium</b> - Show subscription status\n"
            "• <b>Help</b> - Show available features\n\n"
            "⭐️ <b>Premium:</b>\n"
            "• Text\n"
            "• Text\n"
            "• Text"
        ),
        reply_markup=back_button_kb(callback_data="start"),
    )
    await call.answer()
