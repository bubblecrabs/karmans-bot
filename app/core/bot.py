from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n.core import I18n
from redis.asyncio import Redis

from app.core.config import settings

DIR: Path = Path(__file__).absolute().parent.parent.parent
APP_DIR: Path = Path(__file__).absolute().parent.parent
LOCALES_DIR = f"{APP_DIR}/locales"

bot: Bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

redis: Redis = Redis.from_url(url=settings.REDIS_DSN)

storage: RedisStorage = RedisStorage(
    redis=redis,
    key_builder=DefaultKeyBuilder(prefix="fsm:"),
)

dp: Dispatcher = Dispatcher(storage=storage)

i18n: I18n = I18n(
    path=LOCALES_DIR,
    default_locale=settings.DEFAULT_LANGUAGE,
    domain="messages",
)
