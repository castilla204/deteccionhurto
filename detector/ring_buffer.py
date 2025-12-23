from collections import deque
import time


class BufferCircular:
    """Mantiene los últimos segundos de vídeo en memoria."""

    def __init__(self, segundos_maximos, fps):
        self.segundos_maximos = segundos_maximos
        self.fps = fps
        self.fotogramas_maximos = int(segundos_maximos * fps)
        self.buffer = deque(maxlen=self.fotogramas_maximos)
