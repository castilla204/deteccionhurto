from ultralytics import YOLO


class EstimadorPose:
    """Estima poses corporales para visualización e interpretabilidad."""

    def __init__(self, ruta_modelo="yolov8n-pose.pt", confianza=0.3):
        self.modelo = YOLO(ruta_modelo)
        self.confianza = confianza

    def estimar(self, fotograma):
        resultados = self.modelo(fotograma, conf=self.confianza, verbose=False)
        poses = []

        for resultado in resultados:
            if resultado.keypoints is None:
                continue
            puntos = resultado.keypoints.xy.cpu().numpy()
            for puntos_persona in puntos:
                poses.append(puntos_persona)

        return poses
