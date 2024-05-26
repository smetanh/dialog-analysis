from src.ml.relations_model import run_model
from src.telegram_bot.batching import batch_sending_messages
from src.ml.summarization_model import run
from src.translator.translate import detect_language, translate

from aiogram import Router, html
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

import logging
from collections import deque


router = Router()


@router.message(Command("analysis"))
async def analysis_handler(message: Message, state: FSMContext, model, tokenizer) -> None:
    try:
        data = await state.get_data()

        text = data["data"]
        if len(text) == 0:
            await message.answer("Please send any dialog to the chat!")
        else:
            logging.info(text)
            # language = detect_language(text[0])
            # logging.info(language)
            summary = run(text)
            logging.info("---")

            if len(summary.replace("\n", "")) == 0:
                await message.answer("Please send text!")
            else:
                logging.info("SUMMARY: " + summary)
                language = detect_language(text)

                summary = html.bold("Summary: \n\n") + summary
                summary_local = translate(summary, language)

                await batch_sending_messages(message, summary_local, "reply")

                result = run_model(model, tokenizer, summary, language)

                await state.update_data({
                    "data": deque()
                })

                await batch_sending_messages(message, result, "reply")

    except TypeError:
        await message.answer("Unknown error!")
    except KeyError:
        await message.answer(f"Error, please repeat the command \n{html.bold('/analysis')}")
