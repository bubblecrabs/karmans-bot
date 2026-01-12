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
        f"👥 <b>Number of users:</b> <code>{stats.get('total_users')}</code>\n"
        f"📈 <b>New users today:</b> <code>{stats.get('new_users_today')}</code>\n"
        f"👍 <b>Active users:</b> <code>{stats.get('active_users')}</code>\n"
        f"🚫 <b>Blocked users:</b> <code>{stats.get('banned_users')}</code>\n\n"
        "💳 <b>Payments:</b>\n\n"
        f"📦 <b>Total payments:</b> <code>{stats.get('total_payments')}</code>\n"
        f"🆕 <b>Today payments:</b> <code>{stats.get('payments_today')}</code>\n"
        f"💰 <b>Total revenue:</b> <code>{stats.get('total_revenue')}</code> $USD\n"
        f"💵 <b>Today revenue:</b> <code>{stats.get('revenue_today')}</code> $USD"
    )

    await call.message.edit_text(
        text=stats_message,
        reply_markup=back_button_kb(callback_data="admin"),
    )
    await call.answer()
