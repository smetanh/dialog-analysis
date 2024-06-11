from aiogram.types import Message


async def batch_sending(message: Message, text: str, action: str = "answer" or "reply"):
    batch = 4096

    if len(text) > batch:
        for x in range(0, len(text), batch):
            if action == "answer":
                await message.answer(text[x:x + batch])
            elif action == "reply":
                await message.reply(text[x:x + batch])
    else:
        if action == "answer":
            await message.answer(text)
        elif action == "reply":
            await message.reply(text)