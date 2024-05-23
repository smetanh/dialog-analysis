from src.model_name.relations_model import run_model
from src.tg_bot.batching import batch_sending_messages

from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import logging


router = Router()


def user_prefix(message: Message) -> str:
    default_user_prefix = "Person X"

    if message.forward_origin is not None:
        match str(message.forward_origin.type):
            case "MessageOriginType.CHANNEL":
                message_prefix = message.forward_origin.chat.title
            case "MessageOriginType.USER":
                # logging.info(message.forward_origin)
                message_prefix = message.forward_origin.sender_user.first_name
            case "MessageOriginType.CHAT":
                message_prefix = message.forward_origin.chat.title
            case "MessageOriginType.HIDDEN_USER":
                message_prefix = default_user_prefix
            case _:
                message_prefix = default_user_prefix
    else:
        message_prefix = message.from_user.first_name

    _message = message_prefix + ": " + message.text

    return _message


@router.message(~F.text.startswith("/"))
async def query_handler(message: Message, state: FSMContext) -> None:
    try:
        data = await state.get_data()
        text = data["data"]
        message_with_user_prefix = user_prefix(text)

        # реализовать стек, иначе ебанёт по памяти
        await state.update_data({
            "data": message_with_user_prefix + message.text
        })

    except TypeError:
        await message.answer("Unknown error!")
    except KeyError:
        await message.answer(f"Please enter the command {html.bold('/start')}")
    except MemoryError:
        await message.answer("Ебануло по памяти, сделай стек")
