from aiogram import Router, F, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.model_name.relations_model import load_model, load_tokenizer

import logging

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    try:
        model = load_model()
        tokenizer = load_tokenizer()

        await state.set_data({
            "model": model,
            "tokenizer": tokenizer,
            "data": ""
        })
    except Exception as ex:
        await message.answer(f"{html.bold('Error loading the ML model!')}\n\n{str(ex)}")
