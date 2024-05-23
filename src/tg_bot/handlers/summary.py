from src.model_name.summarization_model import run
from src.tg_bot.batching import batch_sending_messages

from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

import logging

router = Router()


@router.message(Command("summary"))
async def summary_handler(message: Message, state: FSMContext) -> None:
    try:
        logging.info("OK?")
        data = await state.get_data()
        text = data["data"]
        result = run(text)
        await state.update_data({
            "data": ""
        })
        await batch_sending_messages(message, result, "answer")
        # if len(result) > 4096:
        #     for x in range(0, len(result), 4096):
        #         await message.answer(result[x:x + 4096])
        # else:
        #     await message.answer(result)

    except TypeError:
        await message.answer("Unknown error!")
    except KeyError:
        await message.answer(f"Please enter the command {html.bold('/start')}")
