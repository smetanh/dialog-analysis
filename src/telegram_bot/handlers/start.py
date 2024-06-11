from collections import deque

from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


router = Router()


async def init_data(state: FSMContext) -> None:
    await state.set_data({
        "previous_messages": deque()
    })


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Приветствую, {html.bold(message.from_user.full_name)}!\n\n"
                         f"Для анализа диалогов перешлите сообщения в этот чат "
                         f"и выберите команду {html.bold('/analysis')}. "
                         f"После каждого анализа контекст диалогов "
                         f"сбрасывается автоматически.\n"
                         f"Для ручного сброса контекста воспользуйтесь "
                         f"командой {html.bold('/clear')}.")

    try:
        await init_data(state)
    except Exception as ex:
        await message.answer(f"{html.bold('Unexpected error!')}\n\n{str(ex)}")




