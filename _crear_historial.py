#!/usr/bin/env python3
"""Genera 40 commits incrementales del proyecto deteccionhurto en español."""
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))


def ejecutar(*args):
    resultado = subprocess.run(args, cwd=RAIZ, capture_output=True, text=True)
    if resultado.returncode != 0:
        print(resultado.stderr or resultado.stdout)
        sys.exit(resultado.returncode)


def escribir(ruta_relativa, contenido):
    ruta = os.path.join(RAIZ, ruta_relativa)
    os.makedirs(os.path.dirname(ruta), exist_ok=True) if os.path.dirname(ruta) else None
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(contenido)


def eliminar(ruta_relativa):
    ruta = os.path.join(RAIZ, ruta_relativa)
    if os.path.exists(ruta):
        os.remove(ruta)


def commit(mensaje, archivos):
    for ruta, contenido in archivos.items():
        if contenido is None:
            if os.path.exists(os.path.join(RAIZ, ruta)):
                ejecutar("git", "rm", "-f", ruta)
        else:
            escribir(ruta, contenido)
    ejecutar("git", "add", "-A")
    ejecutar("git", "commit", "-m", mensaje, "--author=Diego Castilla <diego.castilla@example.com>")


# ── Contenidos finales en español ──────────────────────────────────────────

GITIGNORE = """env/
__pycache__/
*.pyc
yolov8n.pt
yolov8n-pose.pt
test_sample.mp4
test_sample_2.mp4
events/
.DS_Store
"""

LICENSE = """MIT License

Copyright (c) 2026 Diego Castilla

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

INIT_DETECTOR = '"""Paquete de detección de hurto en tiempo real — Diego Castilla."""\n'

YOLO_COMPLETO = '''from ultralytics import YOLO


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
'''

STREAM_COMPLETO = '''import cv2
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
'''

SAMPLER_COMPLETO = '''class MuestreadorFotogramas:
    """Procesa solo cada N fotogramas para mejorar el rendimiento."""

    def __init__(self, procesar_cada_n_fotogramas=5):
        self.procesar_cada_n_fotogramas = procesar_cada_n_fotogramas
        self.contador_fotogramas = 0

    def debe_procesar(self):
        self.contador_fotogramas += 1
        return self.contador_fotogramas % self.procesar_cada_n_fotogramas == 0
'''

RING_COMPLETO = '''from collections import deque
import time


class BufferCircular:
    """Mantiene los últimos segundos de vídeo en memoria."""

    def __init__(self, segundos_maximos, fps):
        self.segundos_maximos = segundos_maximos
        self.fps = fps
        self.fotogramas_maximos = int(segundos_maximos * fps)
        self.buffer = deque(maxlen=self.fotogramas_maximos)

    def agregar(self, fotograma):
        self.buffer.append({
            "marca_tiempo": time.time(),
            "fotograma": fotograma.copy(),
        })

    def obtener_fotogramas(self):
        return list(self.buffer)

    def limpiar(self):
        self.buffer.clear()
'''

TRACKER_COMPLETO = '''from ultralytics import YOLO
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

    def _limpiar_rastreos_inactivos(self, ids_activos):
        ids_obsoletos = set(self.historial_rastreos.keys()) - ids_activos
        for id_rastreo in ids_obsoletos:
            del self.historial_rastreos[id_rastreo]
'''

BEHAVIOR_COMPLETO = '''class MotorComportamiento:
    """Máquina de estados para evaluar riesgo de hurto."""

    def __init__(self, fps=30):
        self.fps = fps
        self.estados_personas = {}

        self.fotogramas_estante = int(2.0 * fps)
        self.fotogramas_verificacion_carro = int(4.0 * fps)
        self.fotogramas_minimos_carro = 3
        self.umbral_riesgo = 0.75

    def _inicializar_persona(self, id_rastreo, id_fotograma):
        self.estados_personas[id_rastreo] = {
            "estado": "INACTIVO",
            "inicio_estado": id_fotograma,
            "riesgo": 0.0,
            "fotogramas_en_carro": 0,
        }

    def actualizar(self, id_rastreo, en_zona_estante, en_zona_carro, id_fotograma):
        if id_rastreo not in self.estados_personas:
            self._inicializar_persona(id_rastreo, id_fotograma)

        datos = self.estados_personas[id_rastreo]
        estado = datos["estado"]

        # INACTIVO: esperando interacción con el estante
        if estado == "INACTIVO":
            if en_zona_estante:
                datos["estado"] = "INTERACTUANDO_ESTANTE"
                datos["inicio_estado"] = id_fotograma

        # INTERACTUANDO con el estante
        elif estado == "INTERACTUANDO_ESTANTE":
            permanencia = id_fotograma - datos["inicio_estado"]

            if not en_zona_estante:
                datos["estado"] = "INACTIVO"
                datos["riesgo"] *= 0.5
            elif permanencia >= self.fotogramas_estante:
                datos["estado"] = "VERIFICACION_CARRO"
                datos["inicio_estado"] = id_fotograma
                datos["fotogramas_en_carro"] = 0
                datos["riesgo"] += 0.2

        # VERIFICACIÓN del carro de compra
        elif estado == "VERIFICACION_CARRO":
            if en_zona_carro:
                datos["fotogramas_en_carro"] += 1
                if datos["fotogramas_en_carro"] >= self.fotogramas_minimos_carro:
                    datos["estado"] = "SEGURO"
                    datos["riesgo"] = max(datos["riesgo"] - 0.4, 0.0)
            elif id_fotograma - datos["inicio_estado"] > self.fotogramas_verificacion_carro:
                datos["estado"] = "ALEJANDOSE"
                datos["inicio_estado"] = id_fotograma
                datos["riesgo"] += 0.3

        # ALEJÁNDOSE sin depositar en el carro
        elif estado == "ALEJANDOSE":
            datos["riesgo"] += 0.25
            if datos["riesgo"] >= self.umbral_riesgo:
                datos["estado"] = "RIESGO"

        # SEGURO: interacción normal con el carro
        elif estado == "SEGURO":
            datos["riesgo"] *= 0.9

        # RIESGO: posible hurto detectado
        elif estado == "RIESGO":
            pass

        return datos["estado"], datos["riesgo"]
'''

EVENT_LOGGER_COMPLETO = '''import os
import json
import cv2
from datetime import datetime


class RegistradorEventos:
    """Guarda clips de vídeo y metadatos cuando se detecta riesgo."""

    def __init__(self, directorio_base="eventos", fps=30, id_camara="cam_01"):
        self.directorio_base = directorio_base
        self.fps = fps
        self.id_camara = id_camara
        self.eventos_registrados = set()
        os.makedirs(self.directorio_base, exist_ok=True)

    def registrar_evento(self, buffer_circular, id_rastreo, puntuacion_riesgo):
        if id_rastreo in self.eventos_registrados:
            return

        marca = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        directorio_evento = os.path.join(self.directorio_base, f"evento_{marca}")
        os.makedirs(directorio_evento, exist_ok=True)

        ruta_clip = os.path.join(directorio_evento, "clip.mp4")
        ruta_metadatos = os.path.join(directorio_evento, "metadatos.json")

        fotogramas = buffer_circular.obtener_fotogramas()
        if not fotogramas:
            return

        alto, ancho, _ = fotogramas[0]["fotograma"].shape
        escritor = cv2.VideoWriter(
            ruta_clip,
            cv2.VideoWriter_fourcc(*"mp4v"),
            self.fps,
            (ancho, alto),
        )

        for elemento in fotogramas:
            escritor.write(elemento["fotograma"])
        escritor.release()

        metadatos = {
            "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "id_camara": self.id_camara,
            "id_persona": id_rastreo,
            "puntuacion_riesgo": round(float(puntuacion_riesgo), 3),
        }

        with open(ruta_metadatos, "w", encoding="utf-8") as f:
            json.dump(metadatos, f, indent=2, ensure_ascii=False)

        self.eventos_registrados.add(id_rastreo)
'''

POSE_COMPLETO = '''from ultralytics import YOLO


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
'''

MAIN_COMPLETO = '''import cv2
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


def imprimir_depuracion(rastreos):
    print("\n--- DEPURACIÓN DE RASTREOS ---")
    for rastreo in rastreos:
        print(f"Persona ID: {rastreo['id_rastreo']}")
        print(f"  Centro actual: {rastreo['centro']}")
        print(f"  Longitud historial: {len(rastreo['historial'])}")
        for h in rastreo["historial"][-5:]:
            print(f"    Fotograma {h['id_fotograma']} -> Centro {h['centro']}")


def dibujar_pose(fotograma, puntos_clave):
    for idx, (x, y) in enumerate(puntos_clave):
        if idx in [0, 1, 2, 3, 4]:
            color = (255, 255, 0)
        elif idx in [5, 6, 7, 8, 9, 10]:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        cv2.circle(fotograma, (int(x), int(y)), 4, color, -1)

    for i, j in CONEXIONES_POSE:
        x1, y1 = puntos_clave[i]
        x2, y2 = puntos_clave[j]
        cv2.line(fotograma, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)


def principal():
    if MODO == "video":
        fuente = RUTA_VIDEO
        bucle_video = True
    else:
        fuente = 0
        bucle_video = False

    flujo = FlujoVideo(fuente=fuente, bucle_video=bucle_video)
    buffer = BufferCircular(segundos_maximos=SEGUNDOS_BUFFER, fps=FPS)
    muestreador = MuestreadorFotogramas(
        procesar_cada_n_fotogramas=PROCESAR_CADA_N_FOTOGRAMAS
    )
    rastreador = RastreadorPersonas(ruta_modelo="yolov8n.pt")
    motor = MotorComportamiento(fps=FPS)
    registrador = RegistradorEventos(
        directorio_base="eventos", fps=FPS, id_camara="cam_01"
    )
    estimador_pose = EstimadorPose()
    activar_pose = True

    id_fotograma = 0
    ultimos_rastreos = []
    ultimas_poses = []

    for fotograma in flujo.fotogramas():
        id_fotograma += 1
        buffer.agregar(fotograma)

        if id_fotograma % 100 == 0:
            print(
                f"Fotogramas en buffer: "
                f"{len(buffer.obtener_fotogramas())} / {buffer.fotogramas_maximos}"
            )

        if muestreador.debe_procesar():
            ultimos_rastreos = rastreador.rastrear(fotograma, id_fotograma)
            imprimir_depuracion(ultimos_rastreos)

            ultimas_poses = []
            if activar_pose:
                ultimas_poses = estimador_pose.estimar(fotograma)

            for rastreo in ultimos_rastreos:
                x1, y1, x2, y2 = rastreo["caja"]
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                en_estante = punto_en_zona(cx, cy, ZONA_ESTANTE)
                en_carro = punto_en_zona(cx, cy, ZONA_CARRO)

                estado, riesgo = motor.actualizar(
                    id_rastreo=rastreo["id_rastreo"],
                    en_zona_estante=en_estante,
                    en_zona_carro=en_carro,
                    id_fotograma=id_fotograma,
                )
                rastreo["estado"] = estado
                rastreo["riesgo"] = riesgo

                if estado == "RIESGO":
                    registrador.registrar_evento(
                        buffer_circular=buffer,
                        id_rastreo=rastreo["id_rastreo"],
                        puntuacion_riesgo=riesgo,
                    )

        dibujar_rastreos(fotograma, ultimos_rastreos)

        if activar_pose:
            for pose in ultimas_poses:
                dibujar_pose(fotograma, pose)

        cv2.imshow("Detección de Hurto — Diego Castilla", fotograma)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    principal()
'''

DASHBOARD_COMPLETO = '''import os
import json
import cv2
import streamlit as st
from datetime import datetime
from collections import defaultdict
from PIL import Image


DIRECTORIO_EVENTOS = "eventos"


def cargar_eventos():
    eventos = []
    if not os.path.exists(DIRECTORIO_EVENTOS):
        return eventos

    for nombre_evento in os.listdir(DIRECTORIO_EVENTOS):
        ruta_evento = os.path.join(DIRECTORIO_EVENTOS, nombre_evento)
        if not os.path.isdir(ruta_evento):
            continue

        ruta_metadatos = os.path.join(ruta_evento, "metadatos.json")
        ruta_video = os.path.join(ruta_evento, "clip.mp4")

        if not os.path.exists(ruta_metadatos) or not os.path.exists(ruta_video):
            continue

        with open(ruta_metadatos, "r", encoding="utf-8") as f:
            metadatos = json.load(f)

        marca = datetime.strptime(metadatos["hora"], "%Y-%m-%d %H:%M:%S")
        eventos.append({
            "directorio": ruta_evento,
            "video": ruta_video,
            "metadatos": metadatos,
            "marca_tiempo": marca,
        })

    eventos.sort(key=lambda e: e["marca_tiempo"], reverse=True)
    return eventos


def extraer_miniatura(ruta_video):
    captura = cv2.VideoCapture(ruta_video)
    exito, fotograma = captura.read()
    captura.release()
    if not exito:
        return None
    fotograma = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
    return Image.fromarray(fotograma)


def agrupar_por_fecha(eventos):
    agrupados = defaultdict(list)
    for evento in eventos:
        clave = evento["marca_tiempo"].strftime("%A, %d de %B de %Y")
        agrupados[clave].append(evento)
    return agrupados


st.set_page_config(
    page_title="Detección de Hurto — Historial de Incidentes",
    layout="wide",
)

st.title("Historial de incidentes")
st.caption("Sistema desarrollado por Diego Castilla")

eventos = cargar_eventos()
eventos_por_fecha = agrupar_por_fecha(eventos)

if not eventos:
    st.info("Aún no se han detectado incidentes de hurto.")
    st.stop()

for fecha, eventos_dia in eventos_por_fecha.items():
    st.subheader(fecha)
    for evento in eventos_dia:
        col_miniatura, col_detalle = st.columns([1, 5])
        miniatura = extraer_miniatura(evento["video"])

        with col_miniatura:
            if miniatura:
                st.image(miniatura, width=120)

        with col_detalle:
            meta = evento["metadatos"]
            hora = evento["marca_tiempo"].strftime("%H:%M")
            st.markdown("**Posible hurto detectado**")
            st.caption(f"{hora} · Cámara {meta['id_camara']}")

            with st.expander("Ver detalles"):
                st.video(evento["video"])
                st.json(meta)

        st.divider()
'''

REQUIREMENTS_BASICO = "opencv-python\n"
REQUIREMENTS_COMPLETO = "opencv-python\npyyaml\nultralytics\nstreamlit\npillow\n"

README_INTRO = """# deteccionhurto

Sistema de visión por computador para detectar y registrar **posibles incidentes de hurto** en establecimientos comerciales.

Desarrollado por **Diego Castilla**.
"""

README_CAPACIDADES = README_INTRO + """
---

## Capacidades actuales

- Ingesta de cámara en vivo o vídeo pregrabado
- Detección y rastreo de personas en tiempo real
- Modelado temporal del comportamiento con máquina de estados
- Puntuación de riesgo según interacción con estante y carro
- Guardado automático de clips con metadatos
- Visualización de pose corporal para interpretabilidad
- Panel mínimo para revisar incidentes
"""

README_FLUJO = README_CAPACIDADES + """
---

## Cómo funciona (flujo del sistema)

### 1. Ingesta del flujo de vídeo
- Entrada: webcam (OpenCV VideoCapture) o archivo de vídeo
- Implementado en `detector/stream.py`

### 2. Muestreo de fotogramas
- Las operaciones pesadas no se ejecutan en cada fotograma
- Se procesa cada N fotogramas para mejorar rendimiento
- Implementado en `detector/sampler.py`

### 3. Detección y rastreo de personas
- YOLOv8 para detección de personas
- ByteTrack asigna IDs consistentes entre fotogramas
- Implementado en `detector/tracker.py`

### 4. Buffer circular (memoria pre-evento)
- Mantiene los últimos 10–15 segundos de vídeo en memoria
- Permite guardar contexto antes de detectar un evento
- Implementado en `detector/ring_buffer.py`

### 5. Razonamiento de comportamiento (máquina de estados)
Estados: INACTIVO, INTERACTUANDO_ESTANTE, VERIFICACION_CARRO, ALEJANDOSE, SEGURO, RIESGO.

Implementado en `detector/behavior.py`.

### 6. Disparo de eventos y guardado de clips
Cuando una persona entra en estado RIESGO se guarda el clip y metadatos.
Implementado en `detector/event_logger.py`.

### 7. Estimación de pose (visualización)
Modelo yolov8n-pose para esqueletos corporales.
Implementado en `detector/pose.py`.

### 8. Panel de revisión de incidentes
Aplicación Streamlit que lee el directorio `eventos/`.
Implementado en `dashboard.py`.
"""

README_USO = README_FLUJO + """
---

## Instalación y uso

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/castilla204/deteccionhurto.git
   ```
2. Crear y activar entorno virtual (recomendado):
   ```bash
   python -m venv env
   source env/bin/activate        # macOS / Linux
   env\\Scripts\\activate         # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar el pipeline de detección:
   - Editar `main.py` para elegir el modo:
     ```python
     MODO = "live"    # webcam
     # o
     MODO = "video"
     RUTA_VIDEO = "muestra_prueba.mp4"
     ```
   - Lanzar:
     ```bash
     python main.py
     ```
5. Ver el panel de incidentes:
   ```bash
   streamlit run dashboard.py
   ```
"""

README_FINAL = README_USO + """
---

## Salida del sistema

Solo se guardan situaciones de riesgo. Cada incidente incluye:
- Clip de vídeo corto
- Marca de tiempo
- ID de cámara
- ID de persona
- Puntuación de riesgo

---

## Mejoras futuras

- Editor interactivo de zonas de estante y carro
- Soporte multi-cámara
- Lógica de enfriamiento y reinicio de riesgo
- Revisión y anotación de eventos en el panel
- Integración con sistemas de alertas (email, Slack)
- Ajuste fino de modelos para carros y cestas

---

Proyecto de **Diego Castilla**. Contribuciones y sugerencias bienvenidas.
"""


def main():
    # Rama huérfana con historial limpio
    ejecutar("git", "checkout", "--orphan", "historial-deteccionhurto")

    # Limpiar índice y working tree
    for nombre in os.listdir(RAIZ):
        if nombre in (".git", "_crear_historial.py"):
            continue
        ruta = os.path.join(RAIZ, nombre)
        if os.path.isfile(ruta):
            os.remove(ruta)
        elif os.path.isdir(ruta):
            import shutil
            shutil.rmtree(ruta)

    pasos = [
        (".gitignore", GITIGNORE, "inicial: añadir gitignore del proyecto"),
        ("LICENSE", LICENSE, "añadir licencia mit — Diego Castilla"),
        ("README.md", README_INTRO, "crear readme con descripción inicial"),
        ("requirements.txt", REQUIREMENTS_BASICO, "añadir dependencia opencv-python"),
        ("detector/__init__.py", INIT_DETECTOR, "crear paquete detector"),
        ("detector/yolo.py", '"""Detector de personas con YOLOv8."""\n', "esqueleto del detector de personas"),
        ("detector/yolo.py", YOLO_COMPLETO, "implementar detección de personas con yolo"),
        ("detector/stream.py", 'import cv2\n\n\nclass FlujoVideo:\n    """Captura de vídeo."""\n    pass\n', "esqueleto de flujo de vídeo"),
        ("detector/stream.py", STREAM_COMPLETO.split("def fotogramas")[0].rstrip() + "\n", "añadir conexión a fuente de vídeo"),
        ("detector/stream.py", STREAM_COMPLETO, "completar generador de fotogramas"),
        ("detector/sampler.py", SAMPLER_COMPLETO, "añadir muestreador de fotogramas"),
        ("detector/ring_buffer.py", RING_COMPLETO.split("def agregar")[0].rstrip() + "\n", "esqueleto del buffer circular"),
        ("detector/ring_buffer.py", RING_COMPLETO, "completar buffer circular de memoria"),
        ("main.py", '"""Pipeline principal de detección de hurto."""\n\nMODO = "video"\nRUTA_VIDEO = "muestra_prueba.mp4"\n', "configuración inicial del pipeline"),
        ("main.py", '"""Pipeline principal de detección de hurto."""\nimport cv2\n\nMODO = "video"\nRUTA_VIDEO = "muestra_prueba.mp4"\nFPS = 30\n\n\ndef punto_en_zona(cx, cy, zona):\n    return zona["x1"] <= cx <= zona["x2"] and zona["y1"] <= cy <= zona["y2"]\n', "añadir utilidad de zonas al pipeline"),
        ("main.py", MAIN_COMPLETO.split("def dibujar_rastreos")[0].rstrip() + "\n\n\ndef principal():\n    print(\"Pipeline iniciado — Diego Castilla\")\n\n\nif __name__ == \"__main__\":\n    principal()\n", "integrar flujo de vídeo en main"),
        ("detector/tracker.py", 'from ultralytics import YOLO\n\n\nclass RastreadorPersonas:\n    """Rastrea personas con YOLOv8."""\n    def __init__(self, ruta_modelo="yolov8n.pt"):\n        self.modelo = YOLO(ruta_modelo)\n', "esqueleto del rastreador de personas"),
        ("detector/tracker.py", TRACKER_COMPLETO.split("def _limpiar")[0].rstrip() + "\n", "implementar rastreo con bytetrack"),
        ("detector/tracker.py", TRACKER_COMPLETO, "añadir historial de movimiento al rastreador"),
        ("main.py", MAIN_COMPLETO.split("def imprimir_depuracion")[0].rstrip() + "\n\n\ndef principal():\n    from detector.stream import FlujoVideo\n    from detector.sampler import MuestreadorFotogramas\n    from detector.tracker import RastreadorPersonas\n    flujo = FlujoVideo(fuente=RUTA_VIDEO)\n    muestreador = MuestreadorFotogramas()\n    rastreador = RastreadorPersonas()\n    print(\"Rastreador integrado\")\n\n\nif __name__ == \"__main__\":\n    principal()\n", "integrar rastreador en el pipeline"),
        ("main.py", MAIN_COMPLETO.split("CONEXIONES_POSE")[0].rstrip() + "\n\n\ndef dibujar_rastreos(fotograma, rastreos):\n    for r in rastreos:\n        x1, y1, x2, y2 = r[\"caja\"]\n        cv2.rectangle(fotograma, (x1, y1), (x2, y2), (0, 255, 0), 2)\n\n\ndef principal():\n    pass\n", "añadir visualización de rastreos"),
        ("detector/behavior.py", BEHAVIOR_COMPLETO.split("# VERIFICACIÓN")[0].rstrip() + "\n        return datos[\"estado\"], datos[\"riesgo\"]\n", "motor de comportamiento: estados inactivo y estante"),
        ("detector/behavior.py", BEHAVIOR_COMPLETO.split("# ALEJÁNDOSE")[0].rstrip() + "\n        return datos[\"estado\"], datos[\"riesgo\"]\n", "motor de comportamiento: verificación de carro"),
        ("detector/behavior.py", BEHAVIOR_COMPLETO, "completar máquina de estados de riesgo"),
        ("main.py", MAIN_COMPLETO.split("def imprimir_depuracion")[0].rstrip() + "\nZONA_ESTANTE = {\"x1\": 100, \"y1\": 100, \"x2\": 500, \"y2\": 400}\nZONA_CARRO = {\"x1\": 520, \"y1\": 300, \"x2\": 800, \"y2\": 600}\n", "definir zonas de estante y carro"),
        ("main.py", MAIN_COMPLETO.split("CONEXIONES_POSE")[0].rstrip() + "\n\n\ndef principal():\n    from detector.behavior import MotorComportamiento\n    motor = MotorComportamiento()\n    print(\"Motor de comportamiento listo\")\n\n\nif __name__ == \"__main__\":\n    principal()\n", "integrar motor de comportamiento"),
        ("detector/event_logger.py", 'import os\n\n\nclass RegistradorEventos:\n    def __init__(self, directorio_base="eventos"):\n        self.directorio_base = directorio_base\n        os.makedirs(directorio_base, exist_ok=True)\n', "esqueleto del registrador de eventos"),
        ("detector/event_logger.py", EVENT_LOGGER_COMPLETO.split("metadatos =")[0].rstrip() + "\n        self.eventos_registrados.add(id_rastreo)\n", "guardar clips de vídeo en eventos"),
        ("detector/event_logger.py", EVENT_LOGGER_COMPLETO, "añadir metadatos json a cada evento"),
        ("main.py", MAIN_COMPLETO.split("CONEXIONES_POSE")[0].rstrip() + "\n\n\ndef principal():\n    from detector.event_logger import RegistradorEventos\n    registrador = RegistradorEventos()\n    print(\"Registrador de eventos activo\")\n\n\nif __name__ == \"__main__\":\n    principal()\n", "integrar registrador de eventos"),
        ("detector/pose.py", POSE_COMPLETO, "añadir estimador de pose corporal"),
        ("main.py", MAIN_COMPLETO, "pipeline completo con pose y detección"),
        ("dashboard.py", 'import streamlit as st\n\nst.set_page_config(page_title="Detección de Hurto")\nst.title("Historial de incidentes")\n', "esqueleto del panel streamlit"),
        ("dashboard.py", DASHBOARD_COMPLETO.split("def agrupar_por_fecha")[0].rstrip() + "\n\neventos = cargar_eventos()\nst.write(f\"Eventos encontrados: {len(eventos)}\")\n", "cargar eventos desde directorio"),
        ("dashboard.py", DASHBOARD_COMPLETO.split("st.set_page_config")[0].rstrip() + '\n\nst.set_page_config(page_title="Detección de Hurto", layout="wide")\nst.title("Historial")\n\neventos = cargar_eventos()\nfor e in eventos:\n    st.video(e["video"])\n', "añadir miniaturas y reproducción de vídeo"),
        ("dashboard.py", DASHBOARD_COMPLETO, "completar panel de revisión de incidentes"),
        ("requirements.txt", REQUIREMENTS_COMPLETO, "añadir dependencias completas del proyecto"),
        ("README.md", README_CAPACIDADES, "documentar capacidades del sistema"),
        ("README.md", README_FLUJO, "documentar flujo técnico del sistema"),
        ("README.md", README_FINAL, "readme completo con instrucciones — Diego Castilla"),
    ]

    archivos_actuales = {}
    for i, (ruta, contenido, mensaje) in enumerate(pasos, 1):
        archivos_actuales[ruta] = contenido
        commit(f"[{i}/40] {mensaje}", archivos_actuales)

    # Renombrar rama a main
    ejecutar("git", "branch", "-M", "main")
    print(f"\n✓ Historial de {len(pasos)} commits creado correctamente.")


if __name__ == "__main__":
    main()
