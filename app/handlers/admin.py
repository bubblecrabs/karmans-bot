from typing import Any

from aiogram import F, Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, Chat, MessageOriginChannel
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import AdminFilter
from app.models.channel import Channel
from app.models.user import User
from app.repositories.channels import ChannelRepository
from app.repositories.users import UserRepository
from app.services.admin import AdminService
from app.utils.keyboards import admin_kb, premium_tier_kb, back_button_kb
from app.utils.states import AdminStates

router = Router()

TIER_DAYS: dict[str, int] = {
    "basic": 3,
    "standard": 7,
    "pro": 30,
}


@router.callback_query(F.data == "admin", AdminFilter())
async def admin_callback(call: CallbackQuery) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="⬇️ <b>What do you want to do?</b>",
        reply_markup=admin_kb(),
    )
    await call.answer()


@router.callback_query(F.data == "block_user", AdminFilter())
async def block_user_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="➡️ <b>Enter the Telegram user ID:</b>",
        reply_markup=back_button_kb(callback_data="user_stats"),
    )
    await state.set_state(state=AdminStates.block_user)
    await call.answer()


@router.message(StateFilter(AdminStates.block_user), AdminFilter())
async def block_user_message(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if not message.from_user or not message.text:
        return

    if not message.text.isdigit():
        await message.answer(text="⁉️ <b>Incorrect Telegram user ID.</b>")
        return

    user_id = int(message.text)
    if user_id == message.from_user.id:
        await message.answer(text="❌ <b>You cannot block yourself.</b>")
        return

    admin_service = AdminService(session)
    success: bool = await admin_service.block_user(user_id=user_id)

    await message.answer(
        text=(
            f"✅ <b>User {user_id} has been blocked.</b>"
            if success
            else f"❌ <b>User {user_id} not found.</b>"
        ),
        reply_markup=back_button_kb(callback_data="user_stats"),
    )
    await state.clear()


@router.callback_query(F.data == "unblock_user", AdminFilter())
async def unblock_user_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="➡️ <b>Enter the Telegram user ID:</b>",
        reply_markup=back_button_kb(callback_data="user_stats"),
    )
    await state.set_state(state=AdminStates.unblock_user)
    await call.answer()


@router.message(StateFilter(AdminStates.unblock_user), AdminFilter())
async def unblock_user_message(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if not message.from_user or not message.text:
        return

    if not message.text.isdigit():
        await message.answer(text="⁉️ <b>Incorrect Telegram user ID.</b>")
        return

    user_id = int(message.text)
    admin_service = AdminService(session)
    success: bool = await admin_service.unblock_user(user_id=user_id)

    await message.answer(
        text=(
            f"✅ <b>User {user_id} has been unblocked.</b>"
            if success
            else f"❌ <b>User {user_id} not found.</b>"
        ),
        reply_markup=back_button_kb(callback_data="user_stats"),
    )
    await state.clear()


@router.callback_query(F.data == "add_premium_user", AdminFilter())
async def add_premium_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="➡️ <b>Enter the Telegram user ID:</b>",
        reply_markup=back_button_kb(callback_data="admin"),
    )
    await state.set_state(state=AdminStates.add_premium_user)
    await call.answer()


@router.message(StateFilter(AdminStates.add_premium_user), AdminFilter())
async def add_premium_message(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if not message.from_user or not message.text:
        return

    if not message.text.isdigit():
        await message.answer(text="⁉️ <b>Incorrect Telegram user ID.</b>")
        return

    user_id = int(message.text)
    user_repo = UserRepository(session)
    user: User | None = await user_repo.get_user_by_user_id(user_id=user_id)
    if not user:
        await message.answer(text=f"❌ <b>User {user_id} not found.</b>")
        return

    await state.update_data(user_id=user_id)
    await state.set_state(state=AdminStates.add_premium_tier)

    await message.answer(
        text="📋 <b>Select a premium subscription type:</b>",
        reply_markup=premium_tier_kb(callback_back="admin"),
    )


@router.callback_query(
    F.data.startswith("premium_tier_"),
    StateFilter(AdminStates.add_premium_tier),
    AdminFilter(),
)
async def add_premium_tier_callback(
    call: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if not isinstance(call.message, Message) or not call.data:
        await call.answer()
        return

    data: dict[str, Any] = await state.get_data()
    user_id = data.get("user_id")

    tier_str: str = call.data.split(sep="_", maxsplit=2)[2]
    days: int = TIER_DAYS.get(tier_str.lower(), 7)

    admin_service = AdminService(session)
    success: bool = await admin_service.add_premium(
        user_id=user_id,  # type: ignore[arg-type]
        days=days,
    )

    await call.message.edit_text(
        text=(
            f"✅ <b>User {user_id} received premium subscription.</b>"
            if success
            else f"❌ <b>Failed to add premium for user {user_id}.</b>"
        ),
        reply_markup=back_button_kb(callback_data="admin"),
    )
    await call.answer()
    await state.clear()


@router.callback_query(F.data == "add_channel", AdminFilter())
async def add_channel_callback(call: CallbackQuery, state: FSMContext) -> None:
    if not isinstance(call.message, Message):
        await call.answer()
        return

    await call.message.edit_text(
        text="➡️ <b>Forward any message from the channel:</b>",
        reply_markup=back_button_kb(callback_data="channel_stats"),
    )
    await state.set_state(state=AdminStates.add_channel)
    await call.answer()


@router.message(StateFilter(AdminStates.add_channel), AdminFilter())
async def add_channel_message(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    bot: Bot,
) -> None:
    if not message.from_user:
        return

    if not message.forward_origin:
        await message.answer(text="❌ <b>This is not a forwarded message.</b>")
        return

    if not isinstance(message.forward_origin, MessageOriginChannel):
        await message.answer(text="❌ <b>The message must be forwarded from the channel.</b>")
        return

    channel: Chat = message.forward_origin.chat
    channel_id: int = channel.id
    channel_title: str = channel.title or "Untitled"
    channel_username: str | None = channel.username
    channel_description: str | None = channel.description

    channel_repo = ChannelRepository(session)
    existing: Channel | None = await channel_repo.get_channel_by_channel_id(channel_id=channel_id)

    if not channel_username:
        try:
            invite_link: str = await bot.export_chat_invite_link(chat_id=channel_id)
        except Exception:
            await message.answer(
                text=(
                    "❌ <b>Unable to create invite link.</b>\n\n"
                    "⚠️ <b>Verify that the bot is the channel administrator.</b>"
                )
            )
            return

    if existing:
        await message.answer(
            text=(
                f"❌ <b>Channel already added:</b>\n\n"
                f"📌 <b>Title:</b> {existing.title}\n"
                f"🆔 <b>ID:</b> <code>{existing.channel_id}</code>\n"
                f"👤 <b>Username:</b> {f'@{existing.username}' if existing.username else 'Private'}\n"
                f"✅ <b>Active:</b> {'Yes' if existing.is_active else 'No'}"
            ),
            reply_markup=back_button_kb(callback_data="channel_stats"),
        )
        await state.clear()
        return

    new_channel: Channel = await channel_repo.create_channel(
        channel_id=channel_id,
        username=channel_username,
        title=channel_title,
        description=channel_description,
        is_active=True,
        invite_link=invite_link,
    )

    await message.answer(
        text=(
            f"✅ <b>Channel successfully added!</b>\n\n"
            f"📌 <b>Title:</b> {new_channel.title}\n"
            f"🆔 <b>ID:</b> <code>{new_channel.channel_id}</code>\n"
            f"👤 <b>Username:</b> {f'@{new_channel.username}' if new_channel.username else 'Private'}\n\n"
            f"⚠️ <b>Important:</b> Add the bot as an administrator to the channel, "
            f"otherwise the subscription check will not work!"
        ),
        reply_markup=back_button_kb(callback_data="channel_stats"),
    )
    await state.clear()
