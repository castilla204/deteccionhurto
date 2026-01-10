from ultralytics import YOLO


class RastreadorPersonas:
    """Rastrea personas con YOLOv8."""
    def __init__(self, ruta_modelo="yolov8n.pt"):
        self.modelo = YOLO(ruta_modelo)
