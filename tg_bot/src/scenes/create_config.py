import logging
from typing import TypedDict

from aiogram.fsm.scene import Scene, on, After
from aiogram import F
from aiogram.types import Message, CallbackQuery

from httpx import AsyncClient, ConnectError, Response

from lib.keyboards import protocols_keyboard


logger = logging.getLogger(__name__)


class FSMData(TypedDict, total=False):
    name: str
    protocol: str


class CreateConfigScene(Scene, state="create_config"):
    @on.callback_query.enter()
    async def on_enter_callback(self, callback_query: CallbackQuery):
        await callback_query.answer()
        await callback_query.message.answer("Enter config name")

    @on.message()
    async def process_config_name(self, message: Message):
        config_name = message.text

        await self.wizard.update_data(name=config_name)

        await message.answer(f"Choose protocol", reply_markup=protocols_keyboard)

    @on.callback_query(F.data.in_({"xray", "awg"}), after=After.exit())
    async def process_protocol(
        self, callback_query: CallbackQuery, client: AsyncClient
    ):
        if not callback_query.message:
            logger.error("No callback query message")

            return

        await callback_query.answer(cache_time=0)
        await callback_query.message.delete_reply_markup()

        data: FSMData = await self.wizard.get_data()
        protocol = callback_query.data

        data_obj = {"name": data.get("name", "undefined"), "protocol": protocol}

        response: Response | None = None

        try:
            response = await client.post("/configs/", json=data_obj)
        except ConnectError as error:
            logger.error(f"No connection with the API server. Details: {error}")

            await callback_query.message.answer("No server connection")

            return

        user = callback_query.from_user

        if response.status_code == 200:
            logger.info(
                f"Successful config generation by {user.full_name} (id={user.id}, username={user.username})"
            )

            await callback_query.message.answer("Success")
        else:
            logger.error(
                f"Something went wrong while config creation by {user.full_name} (id={user.id}, username={user.username})"
            )

            await callback_query.message.answer(
                "Something went wrong. Please try again"
            )
