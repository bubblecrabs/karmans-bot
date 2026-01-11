from faststream.nats import NatsBroker

from app.core.config import settings

broker = NatsBroker(servers=settings.NATS_DSN)


async def start_broker() -> None:
    await broker.start()


async def stop_broker() -> None:
    await broker.stop()
