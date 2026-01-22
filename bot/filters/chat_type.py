from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: ChatType):
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        return message.chat.type == self.chat_type


class OnlyPrivateChatFilter(ChatTypeFilter):
    def __init__(self):
        self.chat_type = ChatType.PRIVATE
