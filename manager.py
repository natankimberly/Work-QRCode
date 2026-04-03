import sqlite3
import sys
import random
import string

def get_db():
    return sqlite3.connect('qrcodes.db')

def generate_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def add_link(url, custom_id=None):
    link_id = custom_id if custom_id else generate_id()
    conn = get_db()
    try:
        conn.execute("INSERT INTO links (id, url) VALUES (?, ?)", (link_id, url))
        conn.commit()
        print(f"Sucesso! Atalho criado.")
        print(f"ID: {link_id}")
        print(f"Destino: {url}")
        print(f"Para ver/imprimir o QR Code acesse: https://seusite.com/qr/{link_id}")
    except sqlite3.IntegrityError:
        print("Erro: Este ID já existe. Escolha outro.")
    finally:
        conn.close()

def list_links():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, url FROM links")
    links = cursor.fetchall()
    conn.close()
    
    print("\n--- Atalhos Ativos ---")
    if not links:
        print("Nenhum atalho encontrado.")
    for link in links:
        print(f"ID: {link[0]} -> URL: {link[1]}")
    print("----------------------\n")

def delete_link(link_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM links WHERE id=?", (link_id,))
    if cursor.fetchone():
        conn.execute("DELETE FROM links WHERE id=?", (link_id,))
        conn.commit()
        print(f"Atalho '{link_id}' excluído com sucesso.")
    else:
        print(f"Erro: Atalho '{link_id}' não existe.")
    conn.close()

def show_help():
    print("\n=== Comandos Disponíveis ===")
    print("Criar link aleatório:  python manager.py criar <url>")
    print("Criar link com nome:   python manager.py criar <url> <id>")
    print("Listar links:          python manager.py listar")
    print("Excluir link:          python manager.py excluir <id>\n")

if __name__ == "__main__":
    # Se o usuário não digitar nada além de 'python manager.py', mostra a ajuda
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
        
    acao = sys.argv[1].lower()
    
    if acao == "criar":
        if len(sys.argv) < 3:
            print("Erro: Faltou a URL. Exemplo: python manager.py criar https://google.com")
        else:
            url = sys.argv[2]
            # Se o usuário digitou uma 4ª palavra, usa como ID personalizado
            custom_id = sys.argv[3] if len(sys.argv) > 3 else None
            add_link(url, custom_id)
            
    elif acao == "listar":
        list_links()
        
    elif acao == "excluir":
        if len(sys.argv) < 3:
            print("Erro: Faltou o ID para excluir. Exemplo: python manager.py excluir promo")
        else:
            link_id = sys.argv[2]
            delete_link(link_id)
            
    else:
        show_help()