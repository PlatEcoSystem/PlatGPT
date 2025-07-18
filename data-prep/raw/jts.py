
import sqlite3

def main():
  
    txt_file = "jokes.txt" 
    db_file = "jokes.db"    
    
 
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

if __name__ == "__main__":
    main()


db.close()