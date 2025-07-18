from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
import os
import openai
import asyncio
from .db_rebuild import rebuild_jokes_db, rebuild_images_db
from .get_db import get_random_joke, get_random_photo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path_joke = os.path.join(BASE_DIR, "data-prep", "processed", "jokes.db")
db_path_photo = os.path.join(BASE_DIR, "data-prep", "processed", "photos.db")

router=Router()

gpt_active_by_chat_id = {}

rebuild_jokes_db()
rebuild_images_db()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("бра здоров, я в групах такие каманды выполняю:\n!фото\n!шутка")


@router.message(F.text == "!ПУК")
async def joke_handler(message: Message):
    question, answer = get_random_joke(db_path_joke)

    await message.answer(question)  # отправляем шутку
    await asyncio.sleep(5)  # ждём 10 секунд
    await message.answer(answer)


@router.message(F.text == '!БРА')
async def photo(message: Message):
    filename = get_random_photo(db_path_photo)  # "photo_2025.jpg"
    photo_path = f"./dev/photos/{filename}"

    photo = FSInputFile(photo_path)  # <-- Вот так создаём файл
    await message.answer_photo(photo)


@router.message(F.text.lower() == "!Z")
async def enable_gpt(message: Message):
    gpt_active_by_chat_id[message.chat.id] = True
    await message.reply("GPT включён 🤖")

@router.message(F.text.lower() == "!V")
async def disable_gpt(message: Message):
    gpt_active_by_chat_id[message.chat.id] = False
    await message.reply("GPT отключён 💤")

async def call_gpt_async(user_input: str) -> str:
    def sync_gpt_call():
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message["content"]
    return await asyncio.to_thread(sync_gpt_call)

@router.message()
async def gpt_message_handler(message: Message):
    if not gpt_active_by_chat_id.get(message.chat.id, False):
        return  # GPT выключен — не отвечаем

    try:
        reply = await call_gpt_async(message.text)
    except Exception as e:
        reply = f"Ошибка GPT: {e}"

    await message.reply(reply)

