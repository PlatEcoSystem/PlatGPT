from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio
import os

token = os.environ.get("TELEGRAM_BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет от Платона через Docker!")

@dp.message(F.text == '!анекдот')
async def joke(message: Message):
    await message.answer('шутка из бд')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
