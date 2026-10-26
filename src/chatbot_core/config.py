"""
config.py: único lugar donde se definen los valores configurables del proyecto.
Los demás archivos hacen: from chatbot_core import config  y usan config.NOMBRE
Los secretos (tokens) NO se escriben aquí: se leen del archivo .env
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Raíz del repositorio: este archivo está en src/chatbot_core/config.py, así que subimos 2 niveles
BASE_DIR = Path(__file__).resolve().parents[2]

# Cargar el .env de la raíz (si no existe no pasa nada: en Docker las variables llegan del entorno)
load_dotenv(BASE_DIR / ".env")

# ---------- Rutas ----------
DATA_DIR = BASE_DIR / "data"
DB_PATH = Path(os.getenv("DB_PATH", DATA_DIR / "ciicap_mock.db"))  # la BD real se indica con la variable DB_PATH
INDEX_DIR = DATA_DIR / "index"  # aquí se guardará el índice de vectores

# ---------- Modelo generativo (Gemma) ----------
HF_TOKEN = os.getenv("HG_TOKEN")  # secreto: vive en el .env
LLM_MODEL_NAME = "google/gemma-3-4b-it"
MAX_NEW_TOKENS = 256   # límite de tokens por respuesta
MAX_HISTORY = 20       # entradas del historial (10 intercambios)
TEMPERATURE = 0.7
TOP_P = 0.9

# ---------- Embeddings y RAG (se usarán en las etapas 3 y 4) ----------
EMBEDDING_MODEL_NAME = "BAAI/bge-m3"
CHUNK_SIZE = 800       # caracteres por fragmento (valor inicial, se ajusta con pruebas)
CHUNK_OVERLAP = 100    # solapamiento entre fragmentos
TOP_K = 4              # fragmentos que se recuperan por pregunta