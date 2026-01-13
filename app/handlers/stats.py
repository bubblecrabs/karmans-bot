from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import AdminFilter
from app.repositories.users import UserRepository
from app.repositories.payments import PaymentRepository
from app.utils.keyboards import back_button_kb

router = Router()


@router.callback_query(F.data == "user_stats", AdminFilter())
async def user_stats_callback(call: CallbackQuery, session: AsyncSession) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    user_repo = UserRepository(session=session)
    stats: dict = await user_repo.get_user_stats()

    await call.message.edit_text(
        text=(
            "📊 <b>Statistics:</b>\n\n"
            f"👥 <b>Number of users:</b> <code>{stats.get('total_users')}</code>\n"
            f"📈 <b>New users today:</b> <code>{stats.get('new_users_today')}</code>\n"
            f"👍 <b>Active users:</b> <code>{stats.get('active_users')}</code>\n"
            f"🚫 <b>Blocked users:</b> <code>{stats.get('banned_users')}</code>"
        ),
        reply_markup=back_button_kb(callback_data="admin"),
    )
    await call.answer()


@router.callback_query(F.data == "payment_stats", AdminFilter())
async def payment_stats_callback(call: CallbackQuery, session: AsyncSession) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    payment_repo = PaymentRepository(session=session)
    stats: dict = await payment_repo.get_payment_stats()

    await call.message.edit_text(
        text=(
            "💳 <b>Payments:</b>\n\n"
            f"📦 <b>Total payments:</b> <code>{stats.get('total_payments')}</code>\n"
            f"🆕 <b>Today payments:</b> <code>{stats.get('payments_today')}</code>\n\n"
            f"💰 <b>Total revenue XTR:</b> <code>{stats.get('total_revenue_xtr'):.2f}</code>\n"
            f"💵 <b>Today revenue XTR:</b> <code>{stats.get('revenue_today_xtr'):.2f}</code>\n\n"
            f"💰 <b>Total revenue USD:</b> <code>{stats.get('total_revenue_usd'):.2f}</code>\n"
            f"💵 <b>Today revenue USD:</b> <code>{stats.get('revenue_today_usd'):.2f}</code>"
        ),
        reply_markup=back_button_kb(callback_data="admin"),
    )
    await call.answer()
