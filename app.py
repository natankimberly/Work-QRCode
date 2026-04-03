from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, StreamingResponse
import sqlite3
import qrcode
import io

app = FastAPI()

def get_url(link_id: str):
    conn = sqlite3.connect('qrcodes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM links WHERE id=?", (link_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

@app.get("/{link_id}")
async def redirect_to_url(link_id: str):
    url = get_url(link_id)
    if url:
        return RedirectResponse(url=url)
    raise HTTPException(status_code=404, detail="Atalho não encontrado")

@app.get("/qr/{link_id}")
async def get_qr_image(link_id: str):
    url = get_url(link_id)
    if not url:
        raise HTTPException(status_code=404, detail="Atalho não encontrado")
    
    # Gera a imagem do QR Code em memória
    full_shortcut_url = f"https://workqrcode.appevolua.com/{link_id}" 
    
    img = qrcode.make(full_shortcut_url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return StreamingResponse(buf, media_type="image/png")