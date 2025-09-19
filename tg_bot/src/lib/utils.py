from aiogram import Dispatcher
from aiogram.fsm.scene import SceneRegistry

from httpx import AsyncClient

from lib.middleware import DALMiddleware
from scenes import CreateConfigScene, DefaultScene, default_router, ManageConfigsScene


def create_dispatcher(client: AsyncClient, chat_id: int) -> Dispatcher:
    dispatcher = Dispatcher(client=client)

    default_router.message.middleware(DALMiddleware(chat_id))
    default_router.message.register(DefaultScene.as_handler())

    dispatcher.include_routers(default_router)

    registry = SceneRegistry(dispatcher)

    registry.add(DefaultScene, CreateConfigScene, ManageConfigsScene)

    return dispatcher
