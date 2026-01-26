from os import environ as env

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from .bot import BotConfig
from .database import DbConfig
from .server import ServerConfig


class Config(BaseModel):
    server: ServerConfig = Field(default_factory=lambda: ServerConfig(**env))
    database: DbConfig = Field(default_factory=lambda: DbConfig(**env))
    bot: BotConfig = Field(default_factory=lambda: BotConfig(**env))


config = Config()
