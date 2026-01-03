"""Pipeline principal de detección de hurto."""
import cv2

MODO = "video"
RUTA_VIDEO = "muestra_prueba.mp4"
FPS = 30


def punto_en_zona(cx, cy, zona):
    return zona["x1"] <= cx <= zona["x2"] and zona["y1"] <= cy <= zona["y2"]
