from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, StreamingResponse
import sqlite3
import qrcode
import io
import os

app = FastAPI()

DOMAIN = os.getenv("DOMAIN", "http://localhost:8000")

def get_db_connection():
    os.makedirs("dados", exist_ok=True)
    return sqlite3.connect('dados/qrcodes.db')

def get_url_and_register_click(link_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT url FROM links WHERE id=?", (link_id,))
    result = cursor.fetchone()
    
    if result:
        cursor.execute("UPDATE links SET clicks = clicks + 1 WHERE id=?", (link_id,))
        conn.commit()
        conn.close()
        return result[0]
        
    conn.close()
    return None

@app.get("/{link_id}")
async def redirect_to_url(link_id: str):
    if link_id == "favicon.ico":
        raise HTTPException(status_code=404)
        
    url = get_url_and_register_click(link_id)
    if url:
        return RedirectResponse(url=url)
    raise HTTPException(status_code=404, detail="Atalho não encontrado")

@app.get("/qr/{link_id}")
async def get_qr_image(link_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM links WHERE id=?", (link_id,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        raise HTTPException(status_code=404, detail="Atalho não encontrado")
    
    full_shortcut_url = f"{DOMAIN}/{link_id}" 
    
    img = qrcode.make(full_shortcut_url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/png")