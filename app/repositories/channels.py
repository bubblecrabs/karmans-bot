from collections.abc import AsyncGenerator, Sequence

from sqlalchemy import select, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.channel import Channel


class ChannelRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def create_channel(
        self,
        channel_id: int,
        username: str | None,
        title: str,
        description: str | None,
        is_active: bool = True,
        invite_link: str | None = None,
    ) -> Channel:
        channel = Channel(
            channel_id=channel_id,
            username=username,
            title=title,
            description=description,
            is_active=is_active,
            invite_link=invite_link,
        )
        self.session.add(instance=channel)
        await self.session.flush()
        await self.session.refresh(instance=channel)
        return channel

    async def update_channel(
        self,
        channel: Channel,
        username: str | None = None,
        title: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
        invite_link: str | None = None,
    ) -> Channel:
        if username is not None:
            channel.username = username
        if title is not None:
            channel.title = title
        if description is not None:
            channel.description = description
        if is_active is not None:
            channel.is_active = is_active
        if invite_link is not None:
            channel.invite_link = invite_link

        await self.session.flush()
        await self.session.refresh(instance=channel)
        return channel

    async def delete_channel(self, channel_id: int) -> bool:
        stmt = delete(table=Channel).where(Channel.channel_id == channel_id)
        result = await self.session.execute(statement=stmt)
        return getattr(result, "rowcount", 0) > 0

    async def get_channel_by_channel_id(self, channel_id: int) -> Channel | None:
        stmt = select(Channel).where(Channel.channel_id == channel_id)
        result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_channel_by_username(self, username: str) -> Channel | None:
        stmt = select(Channel).where(Channel.username == username)
        result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_all_channels(self, batch_size: int = 1000) -> AsyncGenerator[Channel | None]:
        stmt = select(Channel).execution_options(
            yield_per=batch_size,
            stream_results=True,
        )
        stream = await self.session.stream_scalars(statement=stmt)

        async for channel in stream:
            yield channel

    async def get_active_channels(self) -> Sequence[Channel]:
        stmt = select(Channel).where(Channel.is_active == True)  # noqa: E712
        result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_active_channel_ids(self) -> Sequence[int]:
        stmt = select(Channel.channel_id).where(Channel.is_active == True)  # noqa: E712
        result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def set_channel_active(self, channel_id: int, is_active: bool) -> Channel | None:
        stmt = (
            update(table=Channel)
            .where(Channel.channel_id == channel_id)
            .values(is_active=is_active)
            .returning(Channel)
        )
        result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def set_channels_inactive(self, channel_ids: list[int]) -> Sequence[int]:
        stmt = (
            update(table=Channel)
            .where(Channel.channel_id.in_(other=channel_ids))
            .values(is_active=False)
            .returning(Channel.channel_id)
        )
        result = await self.session.execute(statement=stmt)
        return result.scalars().all()

    async def get_channel_stats(self) -> dict[str, int]:
        stmt = select(
            func.count(Channel.id).label("total_channels"),
            func.count(func.nullif(Channel.is_active, False)).label("active_channels"),
            func.count(func.nullif(Channel.is_active, True)).label("inactive_channels"),
            func.count(Channel.username).label("public_channels"),
        )

        result = await self.session.execute(statement=stmt)
        row = result.one()

        return {
            "total_channels": row.total_channels,
            "active_channels": row.active_channels,
            "inactive_channels": row.inactive_channels,
            "public_channels": row.public_channels,
        }
