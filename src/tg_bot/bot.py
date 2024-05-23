from handlers import start, analysis, summary

import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv


# model = load_model()
# tokenizer = load_tokenizer()
#
# load_dotenv("../config.env")
# TOKEN = getenv("BOT_TOKEN")
# dp = Dispatcher()
#
#
# async def main() -> None:
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     dp.include_routers(start.router, analysis.router)
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())

# dp = Dispatcher()


class TelegramBot:
    def __init__(self):
        load_dotenv("../config.env")
        self.TOKEN = getenv("BOT_TOKEN")

        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)
        self.bot = None

    async def main(self) -> None:
        self.bot = Bot(token=self.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp.include_routers(start.router, analysis.router, summary.router)

        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = TelegramBot()
    asyncio.run(bot.main())
