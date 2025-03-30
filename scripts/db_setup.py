import sqlite3
import json
import os

DB_PATH = "database/hadith.db"

def create_database():
    os.makedirs("database", exist_ok=True)  # Ensure folder exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Hadith table with an index for faster search
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hadith (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name TEXT,
            hadith_number INTEGER,
            narrator TEXT,
            text TEXT,
            reference TEXT,
            topic TEXT
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_text ON hadith(text)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_topic ON hadith(topic)')
    
    conn.commit()
    conn.close()
    print("Database and Hadith table created successfully.")

def insert_hadith_from_json(json_file):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            hadith_data = json.load(file)

        hadith_list = [
            (
                hadith.get("book_name", "Sahih Bukhari"),
                hadith.get("hadith_number"),
                hadith.get("narrator"),
                hadith.get("text"),
                hadith.get("reference"),
                hadith.get("topic")
            )
            for hadith in hadith_data
        ]
        
        cursor.executemany('''
            INSERT INTO hadith (book_name, hadith_number, narrator, text, reference, topic)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', hadith_list)
        
        conn.commit()
        print("Hadith data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()

def fetch_hadith_by_keyword(keyword):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT hadith_number, narrator, text, reference, topic FROM hadith
        WHERE text LIKE ? OR topic LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%'))
    
    results = cursor.fetchall()
    conn.close()
    
    return results

if __name__ == "__main__":
    create_database()
    insert_hadith_from_json("data/bukhari.json")
    
    # Example usage: Fetch hadiths related to "action"
    keyword = "action"
    hadiths = fetch_hadith_by_keyword(keyword)
    for h in hadiths:
        print(h)
