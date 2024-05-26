import asyncio
import logging
import sys
from os import getenv

from handlers import start, analysis, query, clear
from middlewares.model import ModelMiddleware
from src.ml.relations_model import load_model, load_tokenizer

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv


class TelegramBot:
    def __init__(self):
        load_dotenv("../config.env")
        self.TOKEN = getenv("BOT_TOKEN")
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)
        self.bot = None

    async def main(self) -> None:
        self.bot = Bot(token=self.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp.include_routers(
            start.router,
            analysis.router,
            query.router,
            clear.router
        )
        model = load_model()
        tokenizer = load_tokenizer()
        self.dp.message.middleware(ModelMiddleware(model, tokenizer))
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = TelegramBot()
    asyncio.run(bot.main())
