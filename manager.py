import sqlite3
import sys
import random
import string
import os

DOMAIN = os.getenv("DOMAIN", "http://localhost:8000")

def get_db():
    os.makedirs("dados", exist_ok=True)
    return sqlite3.connect('dados/qrcodes.db')

def generate_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def format_url(url):
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

def add_link(url, custom_id=None):
    url_formatada = format_url(url)
    link_id = custom_id if custom_id else generate_id()
    conn = get_db()
    try:
        conn.execute("INSERT INTO links (id, url, clicks) VALUES (?, ?, 0)", (link_id, url_formatada))
        conn.commit()
        print(f"Sucesso! Atalho criado.")
        print(f"ID: {link_id}")
        print(f"Destino: {url_formatada}")
        print(f"Acesse o QR Code: {DOMAIN}/qr/{link_id}")
    except sqlite3.IntegrityError:
        print("Erro: Este ID já existe. Escolha outro.")
    finally:
        conn.close()

def list_links():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, url, clicks FROM links")
    links = cursor.fetchall()
    conn.close()
    
    print("\n--- Atalhos Ativos ---")
    if not links:
        print("Nenhum atalho encontrado.")
    for link in links:
        acessos = link[2] if link[2] is not None else 0
        print(f"ID: {link[0]} | Acessos: {acessos:03d} -> URL: {link[1]}")
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
    print("Criar link aleatório:  criar link <url>")
    print("Criar link com nome:   criar link <url> <id>")
    print("Listar links:          listar links")
    print("Excluir link:          excluir link <id>\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
        
    acao = sys.argv[1].lower()
    
    if acao == "criar":
        if len(sys.argv) < 3:
            print("Erro: Faltou a URL. Exemplo: criar link google.com")
        else:
            url = sys.argv[2]
            custom_id = sys.argv[3] if len(sys.argv) > 3 else None
            add_link(url, custom_id)
            
    elif acao == "listar":
        list_links()
        
    elif acao == "excluir":
        if len(sys.argv) < 3:
            print("Erro: Faltou o ID para excluir. Exemplo: excluir link promo")
        else:
            link_id = sys.argv[2]
            delete_link(link_id)
            
    else:
        show_help()