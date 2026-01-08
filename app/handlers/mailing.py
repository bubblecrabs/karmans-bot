import re
from datetime import datetime
from typing import Any

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.filters.admin import AdminFilter
from app.middlewares.media import MediaGroupMiddleware
from app.utils.keyboards import mailing_kb, back_button_kb, edit_button_kb, mailing_confirm_kb
from app.utils.states import MailingStates

router = Router()
router.message.middleware(MediaGroupMiddleware())


@router.callback_query(F.data == "mailing", AdminFilter())
async def mailing_callback(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="⬇️ <b>What do you want to do?</b>",
        reply_markup=mailing_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "mailing_edit_text", AdminFilter())
async def mailing_edit_text_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="✍️ <b>Send the message text for the mailing:</b>",
        reply_markup=back_button_kb(callback_data="mailing"),
    )
    await state.set_state(state=MailingStates.edit_text)
    await call.answer()


@router.message(StateFilter(MailingStates.edit_text), AdminFilter())
async def mailing_text_received_message(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer(text="❌ <b>Please send text message.</b>")
        return

    if len(message.text) > 1024:
        await message.answer(text="❌ <b>The text is too long. Maximum is 1024 characters.</b>")
        return

    await state.update_data(text=message.text)
    await message.answer(
        text="✅ <b>Text saved!</b>",
        reply_markup=back_button_kb(callback_data="mailing"),
    )


@router.callback_query(F.data == "mailing_edit_media", AdminFilter())
async def mailing_edit_media_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text=("🖼️ <b>Send image for the mailing:</b>"),
        reply_markup=back_button_kb(callback_data="mailing"),
    )
    await state.set_state(state=MailingStates.edit_media)
    await call.answer()


@router.message(StateFilter(MailingStates.edit_media), AdminFilter())
async def mailing_media_received_message(
    message: Message,
    state: FSMContext,
    processed_media_groups: set[str],
) -> None:
    if not message.photo:
        await message.answer(text="❌ <b>Please send images.</b>")
        return

    if message.media_group_id:
        if message.media_group_id in processed_media_groups:
            return

        processed_media_groups.add(message.media_group_id)
        await message.answer(text="❌ <b>Albums are not supported!</b>")
        return

    photo_id: str = message.photo[-1].file_id
    await state.update_data(image=photo_id)
    await message.answer(
        text="✅ <b>Image saved!</b>",
        reply_markup=back_button_kb(callback_data="mailing"),
    )


@router.callback_query(F.data == "mailing_edit_button", AdminFilter())
async def mailing_edit_button_callback(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="⬇️ <b>What do you want to do?</b>",
        reply_markup=edit_button_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "mailing_edit_button_text", AdminFilter())
async def mailing_edit_button_text_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="📝 <b>Send the button text for the mailing:</b>",
        reply_markup=back_button_kb(callback_data="mailing_edit_button"),
    )
    await state.set_state(state=MailingStates.edit_button_text)
    await call.answer()


@router.message(StateFilter(MailingStates.edit_button_text), AdminFilter())
async def mailing_button_text_received_message(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer(text="❌ <b>Please send text message.</b>")
        return

    if len(message.text) > 35:
        await message.answer(text="❌ <b>The text is too long. Maximum is 35 characters.</b>")
        return

    await state.update_data(button_text=message.text)
    await message.answer(
        text="✅ <b>Button text saved!</b>",
        reply_markup=back_button_kb(callback_data="mailing_edit_button"),
    )


@router.callback_query(F.data == "mailing_edit_button_url", AdminFilter())
async def mailing_edit_button_url_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="🔗 <b>Send the button url for the mailing:</b>",
        reply_markup=back_button_kb(callback_data="mailing_edit_button"),
    )
    await state.set_state(state=MailingStates.edit_button_url)
    await call.answer()


@router.message(StateFilter(MailingStates.edit_button_url), AdminFilter())
async def mailing_button_url_received_message(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer(text="❌ <b>Please send text message.</b>")
        return

    url: str = message.text.strip()

    http_pattern = r"^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)$"
    telegram_pattern = r"^(?:https?://)?(?:t\.me|telegram\.me)/[a-zA-Z0-9_]{5,32}(?:/\d+)?(?:\?[a-zA-Z0-9_=&-]+)?$"
    tg_protocol_pattern = r"^tg://[a-zA-Z0-9_/?=&-]+$"

    if not (
        re.match(pattern=http_pattern, string=url)
        or re.match(pattern=telegram_pattern, string=url)
        or re.match(pattern=tg_protocol_pattern, string=url)
    ):
        await message.answer(
            text="❌ <b>Invalid URL format.</b>\n\n"
            "📋 <b>Accepted formats:</b>\n"
            "📌 https://example.com\n"
            "📌 https://t.me/username\n"
            "📌 tg://resolve?domain=username",
            disable_web_page_preview=True,
        )
        return

    await state.update_data(button_url=url)
    await message.answer(
        text="✅ <b>Button URL saved!</b>",
        reply_markup=back_button_kb(callback_data="mailing_edit_button"),
    )


@router.callback_query(F.data == "mailing_edit_schedule", AdminFilter())
async def mailing_edit_schedule_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text=(
            "🗓️ <b>Send the schedule date for the mailing:</b>\n\n"
            "📋 <b>Accepted formats:</b>\n"
            "📌 <code>07.01.2026 21:12</code>\n"
            "📌 <code>15.03.2026 09:30</code>\n\n"
            "⏰ <b>Date and time should be in the future</b>"
        ),
        reply_markup=back_button_kb(callback_data="mailing"),
    )
    await state.set_state(state=MailingStates.edit_schedule)
    await call.answer()


@router.message(StateFilter(MailingStates.edit_schedule), AdminFilter())
async def mailing_edit_schedule_message(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer(text="❌ <b>Please send text message.</b>")
        return

    date_str: str = message.text.strip()

    try:
        scheduled_date: datetime = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer(
            text=(
                "❌ <b>Invalid date format!</b>\n\n"
                "📋 <b>Required format:</b>\n"
                "📌 <code>DD.MM.YYYY HH:MM</code>"
            )
        )
        return

    current_date: datetime = datetime.now()
    if scheduled_date <= current_date:
        await message.answer(text="❌ <b>Date must be in the future!</b>")
        return

    await state.update_data(schedule=date_str)
    await message.answer(
        text="✅ <b>Schedule date saved!</b>",
        reply_markup=back_button_kb(callback_data="mailing"),
    )


@router.callback_query(F.data == "mailing_preview", AdminFilter())
async def mailing_preview_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    data: dict[str, Any] = await state.get_data()

    text: str | None = data.get("text")
    image: str | None = data.get("image")
    button_text: str | None = data.get("button_text")
    button_url: str | None = data.get("button_url")
    schedule: str | None = data.get("schedule")

    if not text:
        await call.answer(text="❌ Message text is required!", show_alert=True)
        return

    reply_markup = None
    if button_text and button_url:
        reply_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=button_text, url=button_url)]]
        )

    schedule_info = ""
    if schedule:
        try:
            scheduled_date: datetime = datetime.strptime(schedule, "%d.%m.%Y %H:%M")
            schedule_info = f"\n\n📅 <b>Scheduled for:</b> <code>{scheduled_date.strftime(format='%d.%m.%Y at %H:%M')}</code>"
        except ValueError:
            schedule_info = "\n\n⚡ <b>Send immediately</b>"
    else:
        schedule_info = "\n\n⚡ <b>Send immediately</b>"

    await call.message.answer(text=f"👁️ <b>Mailing Preview:</b>{schedule_info}\n")

    if image:
        await call.message.answer_photo(photo=image, caption=text, reply_markup=reply_markup)
    else:
        await call.message.answer(text=text, reply_markup=reply_markup)

    await call.answer()


@router.callback_query(F.data == "mailing_clear", AdminFilter())
async def mailing_clear_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await state.update_data(
        text=None,
        image=None,
        button_text=None,
        button_url=None,
        schedule=None,
    )

    await call.answer(text="🗑️ Mailing data cleared!", show_alert=True)


@router.callback_query(F.data == "mailing_send", AdminFilter())
async def mailing_send_callback(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="📬 <b>Are you sure you want to start the mailing?</b>",
        reply_markup=mailing_confirm_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "mailing_start", AdminFilter())
async def mailing_start_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    mailing_data: dict[str, Any] = await state.get_data()
    text: str | None = mailing_data.get("text")

    if not text:
        await call.answer(text="❌ Message text is required!", show_alert=True)
        return

    # schedule: str | None = mailing_data.get("schedule")
    #
    # if schedule:
    #     scheduled_time: datetime = datetime.strptime(schedule, "%d.%m.%Y %H:%M")
    #     task = ""
    # else:
    #     task = ""

    await call.message.edit_text(
        text="✅ <b>Mailing started!</b>",
        reply_markup=back_button_kb(callback_data="mailing"),
    )
    await call.answer()
