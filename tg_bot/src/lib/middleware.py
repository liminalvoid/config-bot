from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus

import logging


class DALMiddleware(BaseMiddleware):
    def __init__(self, chat_id) -> None:
        self.chat_id = chat_id
        self.logger = logging.getLogger(__name__)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        restricted = [
            ChatMemberStatus.KICKED,
            ChatMemberStatus.LEFT,
            ChatMemberStatus.RESTRICTED,
        ]

        bot = event.bot

        if event.chat.type != 'private':
            return

        if not bot:
            self.logger.error("No bot instance")

            return

        user = event.from_user

        if not user:
            self.logger.error("No user")

            return

        chat_member = await bot.get_chat_member(self.chat_id, user.id)

        if chat_member.status in restricted:
            self.logger.info(
                f"{user.first_name} {user.last_name} (id={user.id}, username={user.username}) has no access (not in group)"
            )

            return

        return await handler(event, data)
