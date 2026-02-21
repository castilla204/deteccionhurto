import cv2
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
    print("
--- DEPURACIÓN DE RASTREOS ---")
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
