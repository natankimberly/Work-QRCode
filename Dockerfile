FROM python:3.9-slim

WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt .
COPY *.py ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Inicializa o banco de dados
RUN python database.py

# --- A MÁGICA DOS COMANDOS SIMPLIFICADOS ---
# Cria os scripts executáveis globais no Linux
RUN echo '#!/bin/bash\nif [ "$1" == "link" ]; then python /app/manager.py criar "$2" "$3"; else echo "Use: criar link <url> [nome]"; fi' > /usr/local/bin/criar && \
    echo '#!/bin/bash\nif [ "$1" == "links" ]; then python /app/manager.py listar; else echo "Use: listar links"; fi' > /usr/local/bin/listar && \
    echo '#!/bin/bash\nif [ "$1" == "link" ]; then python /app/manager.py excluir "$2"; else echo "Use: excluir link <nome>"; fi' > /usr/local/bin/excluir && \
    chmod +x /usr/local/bin/criar /usr/local/bin/listar /usr/local/bin/excluir

# Expõe a porta do servidor web
EXPOSE 8000

# Inicia o servidor web
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]