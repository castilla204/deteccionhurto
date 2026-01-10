from ultralytics import YOLO
from collections import deque


class RastreadorPersonas:
    """Detecta y rastrea personas con YOLOv8 y ByteTrack."""

    def __init__(
        self,
        ruta_modelo="yolov8n.pt",
        umbral_confianza=0.4,
        config_rastreador="bytetrack.yaml",
        historial_maximo=30,
    ):
        self.modelo = YOLO(ruta_modelo)
        self.umbral_confianza = umbral_confianza
        self.id_clase_persona = 0
        self.config_rastreador = config_rastreador
        self.historial_maximo = historial_maximo
        self.historial_rastreos = {}

    def _obtener_centro(self, caja):
        x1, y1, x2, y2 = caja
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        return cx, cy

    def rastrear(self, fotograma, id_fotograma):
        resultados = self.modelo.track(
            fotograma,
            persist=True,
            tracker=self.config_rastreador,
            verbose=False,
        )

        personas_rastreadas = []
        ids_activos = set()

        for resultado in resultados:
            cajas = resultado.boxes
            if cajas is None:
                continue

            for caja in cajas:
                id_clase = int(caja.cls[0])
                confianza = float(caja.conf[0])

                if id_clase != self.id_clase_persona:
                    continue
                if confianza < self.umbral_confianza:
                    continue
                if caja.id is None:
                    continue

                id_rastreo = int(caja.id[0])
                ids_activos.add(id_rastreo)

                x1, y1, x2, y2 = map(int, caja.xyxy[0])
                caja_bbox = [x1, y1, x2, y2]
                centro = self._obtener_centro(caja_bbox)

                if id_rastreo not in self.historial_rastreos:
                    self.historial_rastreos[id_rastreo] = deque(
                        maxlen=self.historial_maximo
                    )

                self.historial_rastreos[id_rastreo].append({
                    "id_fotograma": id_fotograma,
                    "caja": caja_bbox,
                    "centro": centro,
                })

                personas_rastreadas.append({
                    "id_rastreo": id_rastreo,
                    "caja": caja_bbox,
                    "centro": centro,
                    "confianza": confianza,
                    "id_fotograma": id_fotograma,
                    "historial": list(self.historial_rastreos[id_rastreo]),
                })

        self._limpiar_rastreos_inactivos(ids_activos)
        return personas_rastreadas
