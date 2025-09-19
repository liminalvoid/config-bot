import asyncio
import logging
from os import getenv

from dotenv import load_dotenv

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from httpx import AsyncClient

from lib.utils import create_dispatcher


load_dotenv()

TOKEN = getenv("BOT_TOKEN")
API_URL = getenv("API_URL")
CHAT_ID = getenv("LOOKUP_CHAT_ID")


async def main() -> None:
    if not TOKEN:
        logging.error("No Telegram API token found")

        return

    if not API_URL:
        logging.error("No API URL found")

        return

    if not CHAT_ID or not CHAT_ID.replace("-", "").isdigit():
        logging.error("Chat ID not provided or has incorrect form")

        return

    parsed_chat_id = int(CHAT_ID)

    client = AsyncClient(base_url=API_URL)

    dp = create_dispatcher(client=client, chat_id=parsed_chat_id)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        await client.aclose()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)8s] %(name)30s – %(message)s",
    )

    asyncio.run(main())
