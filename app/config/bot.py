from pydantic import BaseModel


class BotConfig(BaseModel):
    USE_WEBHOOK: bool = False
    BOT_DOMAIN: str = "your.domain.com"
    WEBHOOK_ENDPOINT: str = "/tg/{bot_id}"
    USE_REDIS_STORAGE: bool = False
    BOT_REDIS_DSN: str = "redis://localhost:6379/0"
    TEST_BOT_TOKEN: str | None = None
    TEST_USER_TLG_ID: int | None = None
    CREATE_TEST_USER: bool = False

    ADMINBOT_TOKEN: str
    ADMINBOT_ID: int

    @property
    def webhook_url(self) -> str:
        return f"https://{self.BOT_DOMAIN}{self.WEBHOOK_ENDPOINT}"
