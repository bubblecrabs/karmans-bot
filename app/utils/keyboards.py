from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def start_kb(is_superuser: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Button 1", callback_data="button_1"))
    kb.add(InlineKeyboardButton(text="⭐️ Premium", callback_data="premium"))

    if is_superuser:
        kb.add(InlineKeyboardButton(text="🔐 Admin", callback_data="admin"))

    kb.adjust(2)
    return kb.as_markup()


def back_button_kb(callback_data: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="⬅️ Back", callback_data=callback_data))
    kb.adjust(1)
    return kb.as_markup()


def url_button_kb(text: str | None, url: str | None) -> InlineKeyboardMarkup | None:
    if text is None or url is None:
        return None

    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=text, url=url))
    kb.adjust(1)
    return kb.as_markup()


def menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Option 1", callback_data="option_1"))
    kb.add(InlineKeyboardButton(text="Option 2", callback_data="option_2"))
    kb.add(InlineKeyboardButton(text="⬅️ Back", callback_data="start"))
    kb.adjust(2)
    return kb.as_markup()


def admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📊 Statistics", callback_data="stats"))
    kb.add(InlineKeyboardButton(text="📨 Create mailing", callback_data="create_mailing"))
    kb.add(InlineKeyboardButton(text="📬 Scheduled mailings", callback_data="manage_mailings"))
    kb.add(InlineKeyboardButton(text="🔑 Moderation", callback_data="moderation"))
    kb.add(InlineKeyboardButton(text="⬅️ Back", callback_data="start"))
    kb.adjust(1)
    return kb.as_markup()


def moderation_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="🚫 Ban", callback_data="ban_user_id"))
    kb.add(InlineKeyboardButton(text="✅ Unban", callback_data="unban_user_id"))
    kb.add(InlineKeyboardButton(text="⭐️ Add premium", callback_data="add_premium_user_id"))
    kb.add(InlineKeyboardButton(text="⬅️ Back", callback_data="admin"))
    kb.adjust(2, 1, 1)
    return kb.as_markup()


def moderation_premium_tier_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📦 Basic", callback_data="premium_tier_basic"))
    kb.add(InlineKeyboardButton(text="⭐ Standard", callback_data="premium_tier_standard"))
    kb.add(InlineKeyboardButton(text="💎 Pro", callback_data="premium_tier_pro"))
    kb.add(InlineKeyboardButton(text="⬅️ Back", callback_data="moderation"))
    kb.adjust(2, 1, 1)
    return kb.as_markup()


def mailing_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📝 Edit text", callback_data="mailing_edit_text"))
    kb.add(InlineKeyboardButton(text="🖼️ Edit media", callback_data="mailing_edit_media"))
    kb.add(InlineKeyboardButton(text="🔗 Edit button", callback_data="mailing_edit_button"))
    kb.add(InlineKeyboardButton(text="🗓️ Edit schedule", callback_data="mailing_edit_schedule"))
    kb.add(InlineKeyboardButton(text="👁️ Preview", callback_data="mailing_preview"))
    kb.add(InlineKeyboardButton(text="📤 Send", callback_data="mailing_send"))
    kb.add(InlineKeyboardButton(text="🔄 Refresh", callback_data="mailing_clear"))
    kb.add(InlineKeyboardButton(text="⬅️ Back", callback_data="admin"))
    kb.adjust(2, 2, 2, 1, 1)
    return kb.as_markup()


def mailing_edit_button_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📝 Button Text", callback_data="mailing_edit_button_text"))
    kb.add(InlineKeyboardButton(text="🔗 Button URL", callback_data="mailing_edit_button_url"))
    kb.add(InlineKeyboardButton(text="⬅️ Back", callback_data="create_mailing"))
    kb.adjust(2)
    return kb.as_markup()


def mailing_confirm_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Yes", callback_data="mailing_start"))
    kb.add(InlineKeyboardButton(text="No", callback_data="create_mailing"))
    kb.adjust(2)
    return kb.as_markup()


def manage_mailings_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📋 View Mailings", callback_data="view_mailings"))
    kb.add(InlineKeyboardButton(text="✏️ Update Mailing", callback_data="update_mailing"))
    kb.add(InlineKeyboardButton(text="🗑️ Delete Mailing", callback_data="delete_mailing"))
    kb.add(InlineKeyboardButton(text="⬅️ Back", callback_data="admin"))
    kb.adjust(1)
    return kb.as_markup()
