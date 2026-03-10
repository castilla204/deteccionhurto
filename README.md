# deteccionhurto

Sistema de visión por computador para detectar y registrar **posibles incidentes de hurto** en establecimientos comerciales.

Desarrollado por **Diego Castilla**.

---

## Capacidades actuales

- Ingesta de cámara en vivo o vídeo pregrabado
- Detección y rastreo de personas en tiempo real
- Modelado temporal del comportamiento con máquina de estados
- Puntuación de riesgo según interacción con estante y carro
- Guardado automático de clips con metadatos
- Visualización de pose corporal para interpretabilidad
- Panel mínimo para revisar incidentes

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
