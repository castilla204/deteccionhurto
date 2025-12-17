import cv2
import time


class FlujoVideo:
    """Captura fotogramas desde webcam o archivo de vídeo."""

    def __init__(self, fuente, retraso_reconexion_seg=2, bucle_video=True):
        self.fuente = fuente
        self.retraso_reconexion_seg = retraso_reconexion_seg
        self.bucle_video = bucle_video
        self.captura = None

    def conectar(self):
        if self.captura is not None:
            self.captura.release()

        self.captura = cv2.VideoCapture(self.fuente)

        if not self.captura.isOpened():
            print("No se pudo abrir la fuente de vídeo")
            self.captura = None
            return False

        print("Fuente de vídeo abierta correctamente")
        return True

    def fotogramas(self):
        while True:
            if self.captura is None:
                if not self.conectar():
                    time.sleep(self.retraso_reconexion_seg)
                    continue

            exito, fotograma = self.captura.read()

            if not exito:
                print("Error al leer fotograma")
                self.captura.release()
                self.captura = None

                if self.bucle_video:
                    time.sleep(0.5)
                    continue
                time.sleep(self.retraso_reconexion_seg)
                continue

            yield fotograma
