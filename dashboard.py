import os
import json
import cv2
import streamlit as st
from datetime import datetime
from collections import defaultdict
from PIL import Image


DIRECTORIO_EVENTOS = "eventos"


def cargar_eventos():
    eventos = []
    if not os.path.exists(DIRECTORIO_EVENTOS):
        return eventos

    for nombre_evento in os.listdir(DIRECTORIO_EVENTOS):
        ruta_evento = os.path.join(DIRECTORIO_EVENTOS, nombre_evento)
        if not os.path.isdir(ruta_evento):
            continue

        ruta_metadatos = os.path.join(ruta_evento, "metadatos.json")
        ruta_video = os.path.join(ruta_evento, "clip.mp4")

        if not os.path.exists(ruta_metadatos) or not os.path.exists(ruta_video):
            continue

        with open(ruta_metadatos, "r", encoding="utf-8") as f:
            metadatos = json.load(f)

        marca = datetime.strptime(metadatos["hora"], "%Y-%m-%d %H:%M:%S")
        eventos.append({
            "directorio": ruta_evento,
            "video": ruta_video,
            "metadatos": metadatos,
            "marca_tiempo": marca,
        })

    eventos.sort(key=lambda e: e["marca_tiempo"], reverse=True)
    return eventos


def extraer_miniatura(ruta_video):
    captura = cv2.VideoCapture(ruta_video)
    exito, fotograma = captura.read()
    captura.release()
    if not exito:
        return None
    fotograma = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
    return Image.fromarray(fotograma)

eventos = cargar_eventos()
st.write(f"Eventos encontrados: {len(eventos)}")
