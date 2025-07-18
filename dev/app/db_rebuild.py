import sqlite3
import os
from hashlib import md5
from PIL import Image

def rebuild_jokes_db():
    txt_file = "jokes.txt"
    db_file = "jokes.db"
    if os.path.exists(db_file):
        os.remove(db_file)

    try:
        with open(txt_file, "r", encoding="utf-8") as file:

            lines = [line.strip() for line in file if line.strip()]

            jokes = []
            for line in lines:
                if "|" in line:
                    question, answer = line.split("|", 1)  #
                    jokes.append((question.strip(), answer.strip()))

    except FileNotFoundError:
        print(f"Ошибка: Файл {txt_file} не найден!")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS jokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_sql)
        insert_sql = "INSERT INTO jokes (question, answer) VALUES (?, ?)"
        cursor.executemany(insert_sql, jokes)
        conn.commit()
        print(f"Успешно! Добавлено {len(jokes)} анекдотов в базу данных.")
    except sqlite3.Error as e:
        print(f"Ошибка SQLite: {e}")

    finally:

        if conn:
            conn.close()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PHOTOS_DIR = os.path.join(BASE_DIR, "..", "photos")
DB_DIR = os.path.join(BASE_DIR, "..", "data-prep", "processed")
DB_PATH = os.path.join(DB_DIR, "photos.db")

def rebuild_images_db():
    # Удаляем старую БД, если есть
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️ Старая база удалена.")

    # Создаём директорию для базы, если её нет
    os.makedirs(DB_DIR, exist_ok=True)

    # Создаём новую базу
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            filehash TEXT,
            width INTEGER,
            height INTEGER,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Сканируем папку и добавляем изображения
    count = 0
    for filename in os.listdir(PHOTOS_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(PHOTOS_DIR, filename)

            try:
                with Image.open(filepath) as img:
                    width, height = img.size

                with open(filepath, 'rb') as f:
                    filehash = md5(f.read()).hexdigest()

                cursor.execute('''
                    INSERT INTO photos (filename, filehash, width, height)
                    VALUES (?, ?, ?, ?)
                ''', (filename, filehash, width, height))

                print(f"✅ Добавлено: {filename}")
                count += 1

            except Exception as e:
                print(f"⚠️ Ошибка с {filename}: {e}")

    conn.commit()
    conn.close()
    print(f"📸 Готово! Добавлено {count} изображений в {DB_PATH}")

if __name__ == '__main__':
    print("🚧 Пересборка баз...")
    rebuild_images_db()


