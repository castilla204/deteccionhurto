class MotorComportamiento:
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
        return datos["estado"], datos["riesgo"]
