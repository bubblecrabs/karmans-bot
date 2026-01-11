import asyncio
import logging

from collections.abc import Sequence
from datetime import datetime
from typing import Any

from faststream.nats import NatsRouter

from app.core.bot import bot
from app.core.postgres import get_session
from app.repositories.users import UserRepository
from app.services.mailing import MailingService

logger: logging.Logger = logging.getLogger(name=__name__)

router = NatsRouter()


@router.subscriber(subject="mailing.immediate")
async def handle_immediate_mailing(message_data: dict[str, Any]) -> None:
    mailing_service = MailingService(bot=bot)

    async with get_session() as session:
        user_repo = UserRepository(session=session)
        user_ids: Sequence[int] = await user_repo.get_active_user_ids()

    result: dict[str, int] = await mailing_service.process_mailing(
        message_data=message_data,
        user_ids=user_ids,
    )

    logger.info(msg=f"Mailing completed: {result['success']} success, {result['failed']} failed")


@router.subscriber(subject="mailing.scheduled")
async def handle_scheduled_mailing(message_data: dict[str, Any]) -> None:
    scheduled_time_str: str | None = message_data.get("scheduled_time")

    if not scheduled_time_str:
        logger.error(msg="Scheduled mailing received without scheduled_time")
        return

    scheduled_time: datetime = datetime.fromisoformat(scheduled_time_str)
    now: datetime = datetime.now()

    if scheduled_time <= now:
        logger.warning(msg="Scheduled time is in the past, executing immediately")
    else:
        delay: int | float = (scheduled_time - now).total_seconds()
        logger.info(msg=f"Waiting {delay} seconds until scheduled time")
        await asyncio.sleep(delay)

    mailing_service = MailingService(bot=bot)

    async with get_session() as session:
        user_repo = UserRepository(session=session)
        user_ids: Sequence[int] = await user_repo.get_active_user_ids()

    result: dict[str, int] = await mailing_service.process_mailing(
        message_data=message_data,
        user_ids=user_ids,
    )

    logger.info(
        msg=f"Scheduled mailing completed: {result['success']} success, {result['failed']} failed"
    )
