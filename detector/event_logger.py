import os
import json
import cv2
from datetime import datetime


class RegistradorEventos:
    """Guarda clips de vídeo y metadatos cuando se detecta riesgo."""

    def __init__(self, directorio_base="eventos", fps=30, id_camara="cam_01"):
        self.directorio_base = directorio_base
        self.fps = fps
        self.id_camara = id_camara
        self.eventos_registrados = set()
        os.makedirs(self.directorio_base, exist_ok=True)

    def registrar_evento(self, buffer_circular, id_rastreo, puntuacion_riesgo):
        if id_rastreo in self.eventos_registrados:
            return

        marca = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        directorio_evento = os.path.join(self.directorio_base, f"evento_{marca}")
        os.makedirs(directorio_evento, exist_ok=True)

        ruta_clip = os.path.join(directorio_evento, "clip.mp4")
        ruta_
        self.eventos_registrados.add(id_rastreo)
