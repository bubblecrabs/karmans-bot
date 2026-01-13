from datetime import datetime
from typing import TypedDict, Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    LabeledPrice,
    PreCheckoutQuery,
    SuccessfulPayment,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.bot import bot
from app.models.user import User
from app.services.payment import PaymentService
from app.utils.keyboards import premium_kb, premium_tier_kb, premium_payment_kb

router = Router()


class PremiumTierInfo(TypedDict):
    name: str
    price: int
    duration_days: int


PREMIUM_PRICES: dict[str, PremiumTierInfo] = {
    "premium_tier_basic": {
        "name": "Basic Premium",
        "price": 100,
        "duration_days": 3,
    },
    "premium_tier_standard": {
        "name": "Standard Premium",
        "price": 250,
        "duration_days": 7,
    },
    "premium_tier_pro": {
        "name": "Pro Premium",
        "price": 500,
        "duration_days": 30,
    },
}


@router.callback_query(F.data == "premium")
async def premium_callback(call: CallbackQuery, user: User) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    is_premium: bool = user.is_premium
    premium_until: datetime | None = user.premium_until

    await call.message.edit_text(
        text=(
            "⭐️ <b>Your premium membership is active!</b>\n\n"
            "📅 <b>Valid until:</b> "
            f"<code>{premium_until.strftime(format='%d.%m.%Y %H:%M')}</code>"
            if is_premium and premium_until
            else "⭐️ <b>You don't have premium!</b>"
        ),
        reply_markup=premium_kb(is_premium=is_premium),
    )
    await call.answer()


@router.callback_query(F.data.in_(iterable={"buy_premium", "renew_premium"}))
async def buy_premium_callback(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="⭐️ <b>Select a premium subscription type:</b>",
        reply_markup=premium_tier_kb(callback_back="premium"),
    )
    await call.answer()


@router.callback_query(F.data.startswith("premium_tier_"))
async def payment_method_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message) or not call.data:
        await call.answer()
        return

    premium_tier: str = call.data
    await state.update_data(premium_tier=premium_tier)

    await call.message.edit_text(
        text="💵 <b>Select a payment method:</b>",
        reply_markup=premium_payment_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "payment_telegram_stars")
async def payment_telegram_stars_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    data: dict[str, Any] = await state.get_data()
    premium_tier: str = data.get("premium_tier", "premium_tier_basic")
    tier_info: PremiumTierInfo = PREMIUM_PRICES[premium_tier]

    await bot.send_invoice(
        chat_id=call.message.chat.id,
        title=tier_info["name"],
        description=f"Premium subscription for {tier_info['duration_days']} days",
        payload=f"{premium_tier}_{call.from_user.id}",
        currency="XTR",
        prices=[
            LabeledPrice(
                label=tier_info["name"],
                amount=tier_info["price"],
            )
        ],
    )
    await call.message.edit_text(
        text=("⭐️ <b>Invoice sent!</b>\n\nPlease complete the payment below."),
    )
    await call.answer()


@router.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment_handler(message: Message, session: AsyncSession) -> None:
    payment: SuccessfulPayment | None = message.successful_payment

    if not payment:
        return

    payload_parts: list[str] = payment.invoice_payload.split(sep="_")
    if len(payload_parts) >= 4:
        tier_type = f"{payload_parts[0]}_{payload_parts[1]}_{payload_parts[2]}"
        user_id = int(payload_parts[3])
    else:
        await message.answer(text="❌ <b>Payment processing error.</b>")
        return

    if tier_type not in PREMIUM_PRICES:
        await message.answer(text="❌ <b>Invalid subscription type.</b>")
        return

    tier_info: PremiumTierInfo = PREMIUM_PRICES[tier_type]

    payment_service = PaymentService(session=session)

    success: bool = await payment_service.process_successful_payment(
        user_id=user_id,
        charge_id=payment.telegram_payment_charge_id,
        amount=payment.total_amount,
        currency=payment.currency,
        duration_days=tier_info["duration_days"],
        description=f"{tier_info['name']} subscription",
    )

    if not success:
        await message.answer(text="❌ <b>Error processing payment.</b>")
        return

    await message.answer(
        text=(
            "✅ <b>Payment successful!</b>\n\n"
            f"🎉 <b>{tier_info['name'].title()}</b> subscription activated!\n"
            f"⏳ Valid for <b>{tier_info['duration_days']}</b> days\n\n"
            f"💳 Transaction ID: <code>{payment.telegram_payment_charge_id}</code>"
        )
    )


@router.callback_query(F.data == "payment_crypto")
async def payment_crypto_callback(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.answer()
