import cv2
import time


class VideoStream:
    # Lee frames de webcam o de un vídeo en bucle

    def __init__(self, source, reconnect_delay_sec=2, loop_video=True):
        self.source = source
        self.reconnect_delay_sec = reconnect_delay_sec
        self.loop_video = loop_video
        self.cap = None

    def connect(self):
        if self.cap is not None:
            self.cap.release()

        self.cap = cv2.VideoCapture(self.source)

        if not self.cap.isOpened():
            print("No se pudo abrir la fuente de vídeo")
            self.cap = None
            return False

        print("Fuente de vídeo conectada")
        return True

    def frames(self):
        while True:
            if self.cap is None:
                if not self.connect():
                    time.sleep(self.reconnect_delay_sec)
                    continue

            ret, frame = self.cap.read()

            if not ret:
                print("Fallo al leer frame, reintentando...")
                self.cap.release()
                self.cap = None

                if self.loop_video:
                    time.sleep(0.5)
                    continue

                time.sleep(self.reconnect_delay_sec)
                continue

            yield frame
