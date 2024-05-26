from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from collections import deque


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    try:
        await state.set_data({
            "data": deque()
        })
    except Exception as ex:
        await message.answer(f"{html.bold('Error loading the ML model!')}\n\n{str(ex)}")
