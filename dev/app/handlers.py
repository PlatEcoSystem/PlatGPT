from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
import os
from openai import AsyncOpenAI
import asyncio
from .db_rebuild import rebuild_jokes_db, rebuild_images_db
from .get_db import get_random_joke, get_random_photo


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db_path_joke = os.path.join(BASE_DIR, "data-prep", "processed", "jokes.db")
db_path_photo = os.path.join(BASE_DIR, "data-prep", "processed", "photos.db")
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router=Router()

gpt_active_by_chat_id = {}
chat_histories = {}


rebuild_jokes_db()
rebuild_images_db()



@router.message(CommandStart())
async def start(message: Message):
    await message.answer("бра здоров, я в групах такие каманды выполняю:\n!ПУК\n!БРА\n!Z\n!V")


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


@router.message(F.text == "!Z")
async def enable_gpt(message: Message):
    gpt_active_by_chat_id[message.chat.id] = True
    await message.reply("режим бра")

@router.message(F.text == "!V")
async def disable_gpt(message: Message):
    gpt_active_by_chat_id[message.chat.id] = False
    await message.reply("режим бра выкл")



async def call_gpt_async(user_input: str, chat_id: int) -> str:
    history = chat_histories.get(chat_id, [])
    response = await client.chat.completions.create(  # <--- chat.completions
        model="ft:gpt-4.1-2025-04-14:personal:platgpt:ByE886Wd",
        messages = [{"role": "system",  "content": "Ты — Платон, 14‑летний школьник из Москвы. отвечай развернуто и выражай свои мысли коректно и понятно. Летом живёшь на даче в Клёнах — это твоё любимое место. Твои лучшие друзья — Артвес, Максон и Егор (вы — пацантра), но Макс и Егор уехали в Израиль. Есть ещё брусы из Брусландии (коттеджный посёлок рядом). Пацантра их недолюбливает, но ходит играть с ними в баскет.\n\nСемья Платона: у тебя младший брат Гера ему 8 лет(его лучший друг — Данюня, он же братик Егора), Гера любит играть в игры с Данюней. Папа — Юра. Мама — Злата (у неё дом в Клёнах). Напротив её дома стоит дом Агаши (Агафона) — мачеха Егора, которую пацантра тоже не любит. Плюс ты и Артвес ходили на кружок по биологии.\n\nТы пишешь с ошибками, короткими фразами, используешь свои фразы, но не часто, лишь в контексте прикола: \"пук\", \"гагалы\", \"гул\", \"пагна\", \"каки\", \"курэ\", \"бух\", \"куп\", \"не хач\". Ты добрый, немного глупенький, саркастичный, иногда несёшь чушь: считаешь, что Байден — украинец, а следующий президент США — Мистер Бист. Любишь хуярить заборы брусов ногами.\n\nГлавное — говори как Платон: грубо, по‑дружески, смешно, с ошибками, кратко, часто проявляй любовь к пацантре и упоминай Клёны. еще в с артвесом ходили на кружок по биологии."}] + history[-10:] + [{"role": "user", "content": user_input}],
            temperature=0.6,
            max_tokens=100
        )

    gpt_reply = response.choices[0].message.content


    chat_histories.setdefault(chat_id, []).append({"role": "user", "content": user_input})
    chat_histories[chat_id].append({"role": "assistant", "content": gpt_reply})

    return gpt_reply


@router.message()
async def gpt_message_handler(message: Message):
    if not gpt_active_by_chat_id.get(message.chat.id, False):
        return  # GPT выключен — не отвечаем

    try:
        reply = await call_gpt_async(message.text, message.chat.id)
    except Exception as e:
        reply = f"Ошибка GPT: {e}"

    await message.reply(reply)

