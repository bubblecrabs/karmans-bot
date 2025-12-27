from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


def start_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Button 1", callback_data="button1"))
    kb.add(InlineKeyboardButton(text="Button 2", callback_data="button2"))
    kb.adjust(2)
    return kb.as_markup()
