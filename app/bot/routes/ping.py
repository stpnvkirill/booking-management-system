from aiogram import F, Router
from aiogram.types import Message

router = Router()


async def ping_handler(message: Message):
    await message.answer("pong")


def get_ping_router():
    router.message.register(ping_handler, F.text == "ping")
    return router
