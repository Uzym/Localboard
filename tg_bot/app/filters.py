from aiogram.filters import BaseFilter
from app.config import config
from aiogram.types import Message

class ManageChatFilter(BaseFilter):
    manage_chat = config.manage_chat

    async def __call__(self, message: Message) -> bool:
        print(message.chat.id, str(message.chat.id) in self.manage_chat)
        return str(message.chat.id) in self.manage_chat

