from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


def start_kb(is_superuser: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Button 1", callback_data="button_1"))
    kb.add(InlineKeyboardButton(text="Button 2", callback_data="button_2"))
    if is_superuser:
        kb.add(InlineKeyboardButton(text="Button 3", callback_data="button_3"))
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
