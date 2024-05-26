from aiogram import Router, F, html
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from collections import deque


router = Router()


@router.message(Command("clear"))
async def clear_handler(message: Message, state: FSMContext) -> None:
    try:
        await state.update_data({
            "data": deque()
        })
        _message = "Context has been reset!"

        await message.answer(_message)

    except TypeError:
        await message.answer("Unknown error!")
    except KeyError:
        await message.answer(f"Please enter the command {html.bold('/start')}")
