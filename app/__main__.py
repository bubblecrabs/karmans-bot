import asyncio
import logging

from app.core.bot import bot, dp
from app.core.config import settings
from app.handlers import get_routers
from app.middlewares import get_middlewares
from app.services.posthog import PostHogService


async def on_startup() -> None:
    # Register middlewares
    get_middlewares(dp=dp)

    # Register routers
    dp.include_routers(get_routers())


async def on_shutdown() -> None:
    # Close services
    await PostHogService().close()

    # Close storages
    await dp.storage.close()
    await dp.fsm.storage.close()

    # Delete session and webhook
    await bot.delete_webhook()
    await bot.session.close()


async def main() -> None:
    logging.basicConfig(
        level=settings.LOGGING_LEVEL,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
