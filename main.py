import cv2
from detector.stream import FlujoVideo
from detector.sampler import MuestreadorFotogramas
from detector.tracker import RastreadorPersonas
from detector.ring_buffer import BufferCircular
from detector.behavior import MotorComportamiento
from detector.event_logger import RegistradorEventos
from detector.pose import EstimadorPose


# ── Configuración general ──────────────────────────────────────────────────
MODO = "video"  # "live" para webcam, "video" para archivo
RUTA_VIDEO = "muestra_prueba.mp4"
FPS = 30
SEGUNDOS_BUFFER = 15
PROCESAR_CADA_N_FOTOGRAMAS = 5

ZONA_ESTANTE = {"x1": 100, "y1": 100, "x2": 500, "y2": 400}
ZONA_CARRO = {"x1": 520, "y1": 300, "x2": 800, "y2": 600}

CONEXIONES_POSE = [
    (5, 7), (7, 9), (6, 8), (8, 10), (5, 6),
    (5, 11), (6, 12), (11, 12),
    (11, 13), (13, 15), (12, 14), (14, 16),
]


def punto_en_zona(cx, cy, zona):
    return zona["x1"] <= cx <= zona["x2"] and zona["y1"] <= cy <= zona["y2"]


def dibujar_rastreos(fotograma, rastreos):
    for rastreo in rastreos:
        x1, y1, x2, y2 = rastreo["caja"]
        estado = rastreo.get("estado", "SEGURO")
        riesgo = rastreo.get("riesgo", 0.0)

        if estado == "RIESGO":
            color = (0, 0, 255)
            etiqueta = f"RIESGO {riesgo:.2f}"
            escala_fuente = 1.3
            grosor = 3
        else:
            color = (0, 255, 0)
            etiqueta = "SEGURO"
            escala_fuente = 0.9
            grosor = 2

        cv2.rectangle(fotograma, (x1, y1), (x2, y2), color, grosor)
        cv2.putText(
            fotograma, etiqueta, (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, escala_fuente, color, grosor,
        )


def principal():
    from detector.stream import FlujoVideo
    from detector.sampler import MuestreadorFotogramas
    from detector.tracker import RastreadorPersonas
    flujo = FlujoVideo(fuente=RUTA_VIDEO)
    muestreador = MuestreadorFotogramas()
    rastreador = RastreadorPersonas()
    print("Rastreador integrado")


if __name__ == "__main__":
    principal()
