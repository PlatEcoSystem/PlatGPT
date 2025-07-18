import os
import sqlite3
from hashlib import md5
from PIL import Image


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(BASE_DIR, r"C:\Users\asus\Desktop\prog\PlatGPT\photos")  
DB_PATH = os.path.join(BASE_DIR, r"C:\Users\asus\Desktop\prog\PlatGPT\data-prep\processed\photos.db" )  

def init_db():
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            filehash TEXT,
            width INTEGER,
            height INTEGER,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def update_database():
   
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    existing_files = {row[0] for row in cursor.execute("SELECT filename FROM photos")}
    
    for filename in os.listdir(PHOTOS_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(PHOTOS_DIR, filename)
            
            if filename not in existing_files:
                try:
                    with Image.open(filepath) as img:
                        width, height = img.size
                    
                    with open(filepath, 'rb') as f:
                        filehash = md5(f.read()).hexdigest()
                    
                    cursor.execute('''
                        INSERT INTO photos (filename, filehash, width, height)
                        VALUES (?, ?, ?, ?)
                    ''', (filename, filehash, width, height))
                    print(f"Добавлено: {filename}")
                except Exception as e:
                    print(f"Ошибка с {filename}: {e}")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    print("Инициализация БД...")
    init_db()
    
    print("Сканирование папки photos...")
    update_database()
    
    print("Готово! База данных создана в data-prep/processed/photos.db")