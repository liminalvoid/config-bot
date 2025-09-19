import logging
from typing import TypedDict

from aiogram.fsm.scene import Scene, on, After
from aiogram import F
from aiogram.types import Message, CallbackQuery

from httpx import AsyncClient, ConnectError, Response

from lib.keyboards import protocols_keyboard


logger = logging.getLogger(__name__)


class ManageConfigsScene(Scene, state="manage_configs"):
    @on.callback_query.enter()
    async def on_scene_enter(self, callback_query: CallbackQuery, client: AsyncClient):
        await callback_query.answer(cache_time=0)

        response: Response | None = None

        try:
            response = await client.get("/configs/")
        except ConnectError as error:
            logger.error(f"No connection with the API server. Details: {error}")

            await callback_query.message.answer("No server connection")

            return

        await callback_query.message.answer(response.text)
