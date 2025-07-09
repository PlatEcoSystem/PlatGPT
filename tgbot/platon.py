from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types  import Message
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

# openai_api_key = os.getenv("OPENAI_API_KEY")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(bot_token)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!')

if __name__ == '__main__':
    asyncio.run(main())





