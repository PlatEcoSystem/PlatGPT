from aiogram import Bot, Dispatcher
import asyncio
import os
import openai
from app.handlers import router
from aiogram.fsm.storage.memory import MemoryStorage

token = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
