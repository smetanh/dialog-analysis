from collections import deque

from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


router = Router()


def user_prefix(message: Message) -> str:
    if message.forward_origin is not None:
        # match str(message.forward_origin.type):
        #     case "MessageOriginType.CHANNEL":
        #         username = message.forward_origin.chat.title
        #     case "MessageOriginType.USER":
        #         username = message.forward_origin.sender_user.first_name
        #     case "MessageOriginType.CHAT":
        #         username = message.forward_origin.chat.title
        #     case "MessageOriginType.HIDDEN_USER":
        #         username = "X"
        #     case _:
        username = "Человек"
    else:
        username = message.from_user.first_name

    _message = f'"{username}": {message.text}'

    return _message


def is_first_message(data: dict) -> bool:
    return len(data) == 0


def messages_limit_reached(text: deque) -> bool:
    limit = 1024

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
            text = data["previous_messages"]

        message_with_user_prefix = user_prefix(message)
        text.append(message_with_user_prefix)

        if messages_limit_reached(text):
            await message.answer("Message limit exceeded, last 1024 saved")

        await state.update_data({
            "previous_messages": text
        })

    except TypeError:
        await message.answer("Unknown error!")
    except KeyError:
        await message.answer(f"Error, please repeat the command \n{html.bold('/analysis')}")
    except MemoryError:
        await message.answer("Memory leak")
