import os

import requests
import streamlit as st

# En Docker esta variable apuntará al servicio de la API (por ejemplo http://api:8000)
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Asistente virtual CIICAp")

if "historial" not in st.session_state:
    st.session_state.historial = []  # lista de {"role": "user"/"assistant", "text": "..."}

# Mostrar la conversación acumulada
for m in st.session_state.historial:
    with st.chat_message(m["role"]):
        st.write(m["text"])

pregunta = st.chat_input("Escribe tu pregunta...")
if pregunta:
    with st.chat_message("user"):
        st.write(pregunta)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                r = requests.post(
                    f"{API_URL}/chat",
                    json={"pregunta": pregunta, "historial": st.session_state.historial},
                    timeout=600,  # en CPU Gemma puede tardar mucho
                )
                r.raise_for_status()
                respuesta = r.json()["respuesta"]
                st.write(respuesta)
                st.session_state.historial += [
                    {"role": "user", "text": pregunta},
                    {"role": "assistant", "text": respuesta},
                ]
            except requests.RequestException as e:
                st.error(f"No pude conectar con el servidor: {e}")