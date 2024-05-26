from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ModelMiddleware(BaseMiddleware):
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data["model"] = self.model
        data["tokenizer"] = self.tokenizer
        return await handler(event, data)
