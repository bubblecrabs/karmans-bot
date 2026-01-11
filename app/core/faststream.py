from faststream import FastStream

from app.core.nats import broker
from app.services.subscribers import router

broker.include_router(router)

app = FastStream(broker)
