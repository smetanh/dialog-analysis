import logging

from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from collections import deque

router = Router()


def user_prefix(message: Message) -> str:
    default_user_prefix = 'Person "'

    if message.forward_origin is not None:
        match str(message.forward_origin.type):
            case "MessageOriginType.CHANNEL":
                message_prefix = message.forward_origin.chat.title
            case "MessageOriginType.USER":
                message_prefix = message.forward_origin.sender_user.first_name
            case "MessageOriginType.CHAT":
                message_prefix = message.forward_origin.chat.title
            case "MessageOriginType.HIDDEN_USER":
                message_prefix = 'X"'
            case _:
                message_prefix = 'X"'
    else:
        message_prefix = message.from_user.first_name

    _message = default_user_prefix + message_prefix + '": ' + message.text

    return _message


def is_first_message(data: dict) -> bool:
    return len(data) == 0


def messages_limit_reached(text: deque) -> bool:
    limit = 256

    if len(text) > limit:
        text.popleft()

    return len(text) == limit - 1


@router.message(~F.text.startswith("/") & F.text)
async def query_handler(message: Message, state: FSMContext) -> None:
    try:
        data = await state.get_data()

        if is_first_message(data):
            text = deque()
        else:
            text = data["data"]

        message_with_user_prefix = user_prefix(message)
        text.append(message_with_user_prefix)

        if messages_limit_reached(text):
            await message.answer("Message limit exceeded, last 256 saved")

        await state.update_data({
            "data": text
        })

    except TypeError:
        await message.answer("Unknown error!")
    except KeyError:
        await message.answer(f"Error, please repeat the command \n{html.bold('/analysis')}")
    except MemoryError:
        await message.answer("Memory leak")
