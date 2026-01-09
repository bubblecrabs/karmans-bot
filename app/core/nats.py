from faststream.nats import NatsBroker

from app.core.config import settings

broker = NatsBroker(servers=settings.NATS_DSN)


async def start_broker() -> None:
    """
    Start NATS broker connection.

    Called during application startup to establish
    connection to NATS server.
    """
    await broker.start()


async def stop_broker() -> None:
    """
    Stop NATS broker connection.

    Called during application shutdown to gracefully
    close connection to NATS server.
    """
    await broker.stop()
