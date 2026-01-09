import asyncio
import logging

from faststream import FastStream

from app.core.nats import broker
from app.workers import mailing  # noqa: F401 - Import to register subscribers

app = FastStream(broker)


async def main() -> None:
    """Main worker entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info(msg="Starting NATS worker...")

    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
