from contextlib import asynccontextmanager
from threading import Lock
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from chatbot_core import config

# Por ahora el prompt de sistema vive aquí; en la Etapa 4 se moverá a prompts.py
SYSTEM_PROMPT = (
    "Eres un asistente virtual de una institución educativa. "
    "Responde de manera clara, concisa y profesional en español."
)

lock = Lock()  # el modelo atiende una generación a la vez


class Mensaje(BaseModel):
    role: Literal["user", "assistant"]  # el cliente no puede inyectar mensajes "system"
    text: str


class ChatRequest(BaseModel):
    pregunta: str = Field(min_length=1)
    historial: list[Mensaje] = []


class ChatResponse(BaseModel):
    respuesta: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Importar llm aquí carga Gemma UNA sola vez, al arrancar el servidor
    from chatbot_core import llm
    app.state.llm = llm
    yield


app = FastAPI(title="CIICAp Chatbot API", lifespan=lifespan)


def _formato_gemma(role: str, text: str) -> dict:
    return {"role": role, "content": [{"type": "text", "text": text}]}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    historial = req.historial[-config.MAX_HISTORY:]
    mensajes = [_formato_gemma("system", SYSTEM_PROMPT)]
    mensajes += [_formato_gemma(m.role, m.text) for m in historial]
    mensajes.append(_formato_gemma("user", req.pregunta.strip()))

    with lock:
        respuesta = app.state.llm.generar(mensajes)
    return ChatResponse(respuesta=respuesta)