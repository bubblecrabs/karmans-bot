from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import AdminFilter
from app.services.admin import AdminService
from app.utils.keyboards import back_button_kb

router = Router()


@router.callback_query(F.data == "stats", AdminFilter())
async def stats_callback(call: CallbackQuery, session: AsyncSession) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    stats: dict = await AdminService(session=session).statistics()

    stats_message: str = (
        "📊 <b>Statistics:</b>\n\n"
        f"👥 <b>Number of users:</b> {stats.get('total_users')}\n"
        f"📈 <b>New users today:</b> {stats.get('new_users_today')}\n"
        f"🚫 <b>Blocked users:</b> {stats.get('banned_users')}\n\n"
        f"👤 <b>Last registered:</b> {stats.get('last_user')}\n"
        f"🕒 <b>Registration time:</b> {stats.get('joined_at')}"
    )

    await call.message.edit_text(
        text=stats_message,
        reply_markup=back_button_kb(callback_data="admin"),
    )
    await call.answer()
