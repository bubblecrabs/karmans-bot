from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_kb(is_superuser: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Button 1", callback_data="button_1")
    kb.button(text="Button 2", callback_data="button_2")
    kb.button(text="⭐️ Premium", callback_data="premium")
    kb.button(text="ℹ️ Help", callback_data="help")

    if is_superuser:
        kb.button(text="🔐 Admin", callback_data="admin")

    kb.adjust(2)
    return kb.as_markup()


def back_button_kb(callback_data: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Back", callback_data=callback_data)
    return kb.as_markup()


def url_button_kb(text: str, url: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=text, url=url)
    return kb.as_markup()


def admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="👤 Users", callback_data="user_stats")
    kb.button(text="💳 Payments", callback_data="payment_stats")
    kb.button(text="📢 Channels", callback_data="channel_stats")
    kb.button(text="📨 Create Mailing", callback_data="create_mailing")
    kb.button(text="📬 Scheduled Mailings", callback_data="manage_mailings")
    kb.button(text="⭐️ Add Premium", callback_data="add_premium_user")
    kb.button(text="⬅️ Back", callback_data="start")
    kb.adjust(1)
    return kb.as_markup()


def users_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🔒 Block User", callback_data="block_user")
    kb.button(text="🔓 Unblock User", callback_data="unblock_user")
    kb.button(text="⬅️ Back", callback_data="admin")
    kb.adjust(2, 1)
    return kb.as_markup()


def channels_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📢 Channels", callback_data="channels_page_1")
    kb.button(text="➕ Add Channel", callback_data="add_channel")
    kb.button(text="⬅️ Back", callback_data="admin")
    kb.adjust(1)
    return kb.as_markup()


def mailing_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Edit Text", callback_data="mailing_edit_text")
    kb.button(text="🖼️ Edit Media", callback_data="mailing_edit_media")
    kb.button(text="🔗 Edit Button", callback_data="mailing_edit_button")
    kb.button(text="🗓️ Edit Schedule", callback_data="mailing_edit_schedule")
    kb.button(text="👁️ Preview", callback_data="mailing_preview")
    kb.button(text="📤 Send", callback_data="mailing_send")
    kb.button(text="🔄 Refresh", callback_data="mailing_clear")
    kb.button(text="⬅️ Back", callback_data="admin")
    kb.adjust(2, 2, 2, 1, 1)
    return kb.as_markup()


def mailing_edit_button_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Button Text", callback_data="mailing_edit_button_text")
    kb.button(text="🔗 Button URL", callback_data="mailing_edit_button_url")
    kb.button(text="⬅️ Back", callback_data="create_mailing")
    kb.adjust(2, 1)
    return kb.as_markup()


def mailing_confirm_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📤 Yes", callback_data="mailing_start")
    kb.button(text="⬅️ Back", callback_data="create_mailing")
    kb.adjust(1)
    return kb.as_markup()


def manage_mailings_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📋 View Mailings", callback_data="view_mailings")
    kb.button(text="✏️ Update Mailing", callback_data="update_mailing")
    kb.button(text="🗑️ Delete Mailing", callback_data="delete_mailing")
    kb.button(text="⬅️ Back", callback_data="admin")
    kb.adjust(1)
    return kb.as_markup()


def premium_kb(is_premium: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    if is_premium:
        kb.button(text="⭐️ Renew Premium", callback_data="renew_premium")
    else:
        kb.button(text="⭐️ Buy Premium", callback_data="buy_premium")

    kb.button(text="⬅️ Back", callback_data="start")
    kb.adjust(1)
    return kb.as_markup()


def premium_tier_kb(callback_back: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📦 Basic", callback_data="premium_tier_basic")
    kb.button(text="⭐ Standard", callback_data="premium_tier_standard")
    kb.button(text="💎 Pro", callback_data="premium_tier_pro")
    kb.button(text="⬅️ Back", callback_data=callback_back)
    kb.adjust(2, 1, 1)
    return kb.as_markup()


def premium_payment_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⭐ Telegram Stars", callback_data="payment_telegram_stars")
    kb.button(text="💎 Crypto", callback_data="payment_crypto")
    kb.button(text="⬅️ Back", callback_data="premium")
    kb.adjust(2, 1)
    return kb.as_markup()
