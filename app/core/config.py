from pydantic import PostgresDsn, RedisDsn, NatsDsn
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
    DEFAULT_LANGUAGE: str = "en"
    CHANNEL_IDS: set[int] | None = None

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
        return str(object=dsn)

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
        return str(object=dsn)

    # Nats settings
    NATS_USER: str | None = None
    NATS_PASSWORD: str | None = None
    NATS_HOST: str = "nats"
    NATS_PORT: int = 4222

    @property
    def NATS_DSN(self) -> str:
        dsn: NatsDsn = NatsDsn.build(
            scheme="nats",
            host=self.NATS_HOST,
            port=self.NATS_PORT,
            username=self.NATS_USER,
            password=self.NATS_PASSWORD,
        )
        return str(object=dsn)


settings = Settings()
