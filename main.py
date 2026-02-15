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


def principal():
    from detector.event_logger import RegistradorEventos
    registrador = RegistradorEventos()
    print("Registrador de eventos activo")


if __name__ == "__main__":
    principal()
