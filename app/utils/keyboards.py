from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def start_kb(is_superuser: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Button 1", callback_data="button_1"))
    kb.add(InlineKeyboardButton(text="Button 2", callback_data="button_2"))

    if is_superuser:
        kb.add(InlineKeyboardButton(text="Admin", callback_data="admin"))

    kb.adjust(2)
    return kb.as_markup()


def back_button_kb(callback_data: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="⬅️ Back", callback_data=callback_data))
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
    kb.add(InlineKeyboardButton(text="Statistics", callback_data="stats"))
    kb.add(InlineKeyboardButton(text="Mailing", callback_data="mailing"))
    kb.add(InlineKeyboardButton(text="Manage Users", callback_data="manage_users"))
    kb.add(InlineKeyboardButton(text="⬅️ Back", callback_data="start"))
    kb.adjust(2, 1, 1)
    return kb.as_markup()


def manage_users_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Block user", callback_data="block_user"))
    kb.add(InlineKeyboardButton(text="Unblock user", callback_data="unblock_user"))
    kb.add(InlineKeyboardButton(text="⬅️ Back", callback_data="admin"))
    kb.adjust(2)
    return kb.as_markup()
