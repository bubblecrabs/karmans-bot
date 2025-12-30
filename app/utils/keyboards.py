from collections.abc import Sequence

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _


def create_inline_keyboard(
    buttons: Sequence[tuple[str, str]],
    adjust: int | Sequence[int] = 1,
) -> InlineKeyboardMarkup:
    """
    Create inline keyboard from button definitions.

    Args:
        buttons: Sequence of (text, callback_data) tuples
        adjust: Row width(s) for button layout

    Returns:
        InlineKeyboardMarkup ready to use
    """
    kb = InlineKeyboardBuilder()
    for text, callback_data in buttons:
        kb.add(InlineKeyboardButton(text=_(text), callback_data=callback_data))

    if isinstance(adjust, int):
        kb.adjust(adjust)
    else:
        kb.adjust(*adjust)

    return kb.as_markup()


def start_kb(is_superuser: bool) -> InlineKeyboardMarkup:
    buttons: list[tuple[str, str]] = [
        ("Button 1", "button_1"),
        ("Button 2", "button_2"),
    ]
    if is_superuser:
        buttons.append(("Button 3", "button_3"))

    return create_inline_keyboard(buttons, adjust=2)


def back_button_kb(callback_data: str) -> InlineKeyboardMarkup:
    return create_inline_keyboard(buttons=[("⬅️ Back", callback_data)])


def menu_kb() -> InlineKeyboardMarkup:
    buttons: list[tuple[str, str]] = [
        ("Option 1", "option_1"),
        ("Option 2", "option_2"),
        ("⬅️ Back", "start"),
    ]
    return create_inline_keyboard(buttons, adjust=2)


def lang_kb() -> InlineKeyboardMarkup:
    buttons: list[tuple[str, str]] = [
        ("🇷🇺 Russian", "lang_ru"),
        ("🇺🇦 Ukrainian", "lang_uk"),
        ("🇬🇧 English", "lang_en"),
    ]
    return create_inline_keyboard(buttons, adjust=2)
