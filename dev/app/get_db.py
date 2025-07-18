import sqlite3


def get_random_joke(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT question, answer FROM jokes ORDER BY RANDOM() LIMIT 1;")
    result = cursor.fetchone()

    conn.close()
    return result

def get_random_photo(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM photos ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()  # result — кортеж, например ('photo_2025-07-16_20-37-33.jpg',)
    conn.close()
    if result:
        return result[0]
