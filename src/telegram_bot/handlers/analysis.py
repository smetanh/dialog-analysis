import asyncio

from src.ml.relations_model import Relations
from src.telegram_bot.batching import batch_sending
from src.ml.summarization_model import get_summary
from src.translator.translate import detect_language, translate

from collections import deque
import logging

from aiogram import Router, html
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command


router = Router()


def add_prefixes(output, prefixes) -> str:
    prefixes = tuple(prefixes)
    logging.info("OUTPUT=======================")
    logging.info(output)
    output = output.split("\n")

    for i in range(len(output)):
        output[i] = ", ".join(list(dict.fromkeys(output[i].split(", "))))

    output = tuple(output)

    pattern = ("<b>[%s]:</b> " + "%%s\n") * len(prefixes)
    output = pattern % prefixes % output
    return output


async def get_context(state: FSMContext) -> deque:
    data = await state.get_data()
    text = data["previous_messages"]
    return text


async def clear_context(state: FSMContext) -> None:
    await state.update_data({
        "previous_messages": deque()
    })


def add_header(head: str, body: str) -> str:
    message = html.bold(head) + ":\n\n" + body
    return message


def check_no_translate(text: str, local_language: str) -> str:
    text = text.split("\n")
    for i in range(len(text)):
        text_language = detect_language(text[i])
        if text_language != local_language:
            # logging.info("~~~: " + text[i])
            text[i] = translate(text[i], local_language)
            # logging.info("---: " + text[i])
    return "\n".join(text)


# def add_prefixes(prefixes: tuple, body: str) -> str:
#     body = body.split("\n")
#     for i in range(len(body)):
#         body[i] = ", ".join(set(body[i].split(", ")))
#     body = tuple(body)
#
#     pattern = ("<b>[%s]:</b> " + "%%s\n") * len(prefixes)
#     message = pattern % prefixes % body
#     return message


@router.message(Command("analysis"))
async def analysis_handler(message: Message, state: FSMContext, model, tokenizer) -> None:
    try:
        conversation = await get_context(state)
        logging.info("CONVERSATION=======================")
        logging.info(conversation)
        if conversation:
            summary = get_summary(conversation)
            logging.info("SUMMARY=======================")
            logging.info(summary)
            if summary:
                language = detect_language(conversation)
                logging.info("LANGUAGE=======================")
                logging.info(language)
                summary_local = translate(summary, language)
                summary_local = add_header("Summary", summary_local)
                await batch_sending(message, summary_local, "reply")
                r = Relations(model, tokenizer, conversation)
                relations = r.get_relations()
                logging.info("relations=======================")
                logging.info(relations)
                relations_local = translate(relations, language)
                logging.info("relations_local=======================")
                logging.info(relations_local)
                relations_local = check_no_translate(relations_local, language)
                logging.info("check_no_translate=======================")
                logging.info(relations_local)
                # prefixes = r.get_prefixes()
                logging.info("prefixes=======================")
                # logging.info(prefixes)
                # relations_local = add_prefixes(relations_local, prefixes)
                logging.info("add_prefixes=======================")
                logging.info(relations_local)
                relations_local = add_header("Relations", relations_local)
                await batch_sending(message, relations_local, "reply")
            else:
                await message.answer("Please send text!")
            await clear_context(state)
        else:
            await message.answer("Please send any dialog to the chat!")
    except TypeError:
        await message.answer("Unknown type error!")
    except KeyError:
        await message.answer(f"Error!\nPlease repeat the {html.bold('/analysis')} command after 20s")
