from os import getenv

from aiogram import F
from aiogram.fsm.scene import After, Scene, on
from aiogram.types import CallbackQuery, Message

from lib.keyboards import start_keyboard
from lib.middleware import DALMiddleware

from .create_config import CreateConfigScene
from .manage_configs import ManageConfigsScene


class DefaultScene(
    Scene,
    reset_data_on_enter=True,
    reset_history_on_enter=True,
    callback_query_without_state=True,
):
    """
    Default scene for the bot.

    This scene is used to handle all messages that are not handled by other scenes.
    """

    @on.callback_query(F.data == "new_config", after=After.goto(CreateConfigScene))
    async def on_new_config_callback(self, callback_query: CallbackQuery):
        await callback_query.answer(cache_time=0)
        await callback_query.message.delete_reply_markup()

    @on.callback_query(F.data == "manage_configs", after=After.goto(ManageConfigsScene))
    async def on_manage_configs_callback(self, callback_query: CallbackQuery):
        await callback_query.answer(cache_time=0)
        await callback_query.message.delete_reply_markup()

    @on.message.enter()
    @on.message()
    async def default_handler(self, message: Message):
        await message.answer(
            "Choose an option",
            reply_markup=start_keyboard,
        )


default_router = DefaultScene.as_router()
