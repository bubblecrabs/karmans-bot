import logging

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Bot settings
    BOT_TOKEN: str = "changethis"
    DEBUG: bool = False
    LOGGING_LEVEL: int = logging.INFO

    # Postgres settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"

    @property
    def POSTGRES_DSN(self) -> str:
        dsn: PostgresDsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=self.POSTGRES_DB,
        )
        return str(dsn)

    # Redis settings
    REDIS_USER: str | None = None
    REDIS_PASSWORD: str | None = None
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def REDIS_DSN(self) -> str:
        dsn: RedisDsn = RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            username=self.REDIS_USER,
            password=self.REDIS_PASSWORD,
            path=f"{self.REDIS_DB}",
        )
        return str(dsn)


settings = Settings()
