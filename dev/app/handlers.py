from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.filters import CommandStart
import sqlite3
import os
import openai
import asyncio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path_joke = os.path.join(BASE_DIR, "data-prep", "processed", "jokes.db")
db_path_photo = os.path.join(BASE_DIR, "data-prep", "processed", "images.db")

router=Router()

gpt_active_by_chat_id = {}


def get_random_joke(db_path=db_path_joke):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT question, answer FROM jokes ORDER BY RANDOM() LIMIT 1;")
    result = cursor.fetchone()

    conn.close()
    return result

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("бра здоров, я в групах такие каманды выполняю:\n!фото\n!шутка")


@router.message(F.text == "!шутка")
async def joke_handler(message: Message):
    question, answer = get_random_joke()

    await message.answer(question)  # отправляем шутку
    await asyncio.sleep(5)  # ждём 10 секунд
    await message.answer(answer)

@router.message(F.text == '!фото')
async def photo(message: Message):
    conn = sqlite3.connect(db_path_photo)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM images ORDER BY RANDOM() LIMIT 1")
    photo = cursor.fetchone()
    conn.close()
    if photo:
        await message.answer(photo[0])
    else:
        await message.answer("нет")


@router.message(F.text.lower() == "!го")
async def enable_gpt(message: Message):
    gpt_active_by_chat_id[message.chat.id] = True
    await message.reply("GPT включён 🤖")

@router.message(F.text.lower() == "!пока")
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

