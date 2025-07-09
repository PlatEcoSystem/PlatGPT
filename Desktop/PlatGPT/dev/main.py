from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio
import os

token = os.environ.get("TELEGRAM_BOT_TOKEN")
if not token:
    raise ValueError("Переменная окружения TELEGRAM_BOT_TOKEN не найдена!")

bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("бра здоров, меня надо в групу добав и я смогу писать кленовым пацыкам, вот команды:\n!анекдот\n!пук")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
