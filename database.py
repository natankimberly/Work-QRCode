import sqlite3
import os

def init_db():
    os.makedirs("dados", exist_ok=True)
    conn = sqlite3.connect('dados/qrcodes.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id TEXT PRIMARY KEY,
            url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0
        )
    ''')
    
    try:
        cursor.execute("ALTER TABLE links ADD COLUMN clicks INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado/atualizado na pasta 'dados/'.")