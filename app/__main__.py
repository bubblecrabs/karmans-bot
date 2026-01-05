import asyncio
import logging

from app.core.bot import bot, dp
from app.handlers import setup_routers
from app.middlewares import setup_middlewares
from app.utils.commands import setup_commands, delete_commands


async def on_startup() -> None:
    # Register middlewares
    setup_middlewares(dp=dp)

    # Register routers
    setup_routers(dp=dp)

    # Register commands
    await setup_commands(bot=bot)


async def on_shutdown() -> None:
    # Delete commands
    await delete_commands(bot=bot)

    # Close storages
    await dp.storage.close()
    await dp.fsm.storage.close()

    # Delete session and webhook
    await bot.delete_webhook()
    await bot.session.close()


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
