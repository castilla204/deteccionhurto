# deteccionhurto

Proyecto del **Máster en Inteligencia Artificial** (TFM). Consiste en un sistema de vídeo que analiza el comportamiento de clientes en un pasillo de tienda y avisa cuando algo parece un posible hurto.

Lo fui desarrollando entre **diciembre 2025 y marzo 2026**, poco a poco, módulo a módulo.

**Diego Castilla**

---

## De qué va

La cámara (o un vídeo de prueba) entra en un pipeline que hace lo siguiente:

1. Detecta personas en cada frame procesado.
2. Les asigna un ID y las sigue en el tiempo.
3. Comprueba si entran en la zona del estante y si después pasan por la zona del carro.
4. Si interactúan con el estante pero no van al carro, sube una puntuación de riesgo.
5. Al llegar al umbral, guarda un clip corto con lo que había en memoria (unos 15 s antes) y un JSON con los datos del incidente.

No pretende acusar a nadie automáticamente: la idea es **filtrar y dejar evidencia** para que una persona lo revise. Por eso solo se guardan los casos marcados como riesgo, no el vídeo entero.

---

## Herramientas usadas

| Herramienta | Para qué la usé |
|-------------|-----------------|
| **Python 3** | Todo el proyecto |
| **OpenCV** | Leer webcam/vídeo, pintar cajas y guardar los clips |
| **YOLOv8** (Ultralytics) | Detectar personas en el frame |
| **ByteTrack** | Rastreo con ID estable entre frames |
| **YOLOv8-pose** | Dibujar el esqueleto en pantalla (solo visual, no afecta al riesgo) |
| **Streamlit** | Panel para ver el historial de incidentes |
| **Pillow** | Miniaturas en el dashboard |

Dependencias en `requirements.txt`: `opencv-python`, `ultralytics`, `streamlit`, `pillow`, `pyyaml`.

La primera ejecución descarga los modelos `yolov8n.pt` y `yolov8n-pose.pt`.

---

## Cómo está organizado el código

```
detector/
  stream.py       → captura de vídeo (webcam o archivo)
  sampler.py      → procesa 1 de cada 5 frames (si no, va muy lento)
  tracker.py      → YOLO + ByteTrack
  ring_buffer.py  → últimos 15 s en RAM
  behavior.py     → máquina de estados y puntuación de riesgo
  event_logger.py → guarda clip + metadata.json
  pose.py         → estimación de pose para dibujar
main.py           → une todo el pipeline
dashboard.py      → revisar eventos guardados
```

Estados de la lógica de comportamiento:

`IDLE` → `INTERACTING_WITH_SHELF` → `CART_CHECK` → `MOVING_AWAY` → `RISK`

Si la persona pasa por el carro a tiempo, va a `SAFE` y el riesgo baja.

---

## Instalación

```bash
git clone https://github.com/castilla204/deteccionhurto.git
cd deteccionhurto
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

---

## Uso

En `main.py` eliges la fuente:

```python
MODE = "live"               # webcam
# MODE = "video"
# VIDEO_PATH = "test_sample.mp4"
```

Las zonas del estante y el carro van con coordenadas en píxeles y hay que ajustarlas a mano según la cámara:

```python
SHELF_ZONE = {"x1": 100, "y1": 100, "x2": 500, "y2": 400}
CART_ZONE  = {"x1": 520, "y1": 300, "x2": 800, "y2": 600}
```

```bash
python main.py              # q para salir
streamlit run dashboard.py
```

---

## Qué se guarda

Carpeta `events/event_YYYY_MM_DD_HH_MM_SS/`:

- `clip.mp4`
- `metadata.json` (hora, cámara, persona, risk_score)

---

## Limitaciones y mejoras posibles

- Las zonas son fijas en código, habría que hacer un editor visual.
- Una sola cámara de momento.
- Los carros/cestas no se detectan como objetos; solo hay una zona rectangular.
- Se podría añadir alertas por email o soporte multi-cámara.

---

Diego Castilla — Máster en Inteligencia Artificial — marzo 2026
