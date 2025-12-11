from ultralytics import YOLO


class DetectorPersonas:
    """Detecta personas en un fotograma usando YOLOv8."""

    def __init__(self, ruta_modelo="yolov8n.pt", umbral_confianza=0.4):
        self.modelo = YOLO(ruta_modelo)
        self.umbral_confianza = umbral_confianza
        self.id_clase_persona = 0

    def detectar(self, fotograma):
        resultados = self.modelo(fotograma, verbose=False)
        detecciones = []

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

                x1, y1, x2, y2 = map(int, caja.xyxy[0])
                detecciones.append({
                    "caja": [x1, y1, x2, y2],
                    "confianza": confianza,
                })

        return detecciones
