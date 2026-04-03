import sqlite3

def init_db():
    conn = sqlite3.connect('qrcodes.db')
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
    print("Banco de dados inicializado/atualizado com sucesso.")