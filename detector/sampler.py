class MuestreadorFotogramas:
    """Procesa solo cada N fotogramas para mejorar el rendimiento."""

    def __init__(self, procesar_cada_n_fotogramas=5):
        self.procesar_cada_n_fotogramas = procesar_cada_n_fotogramas
        self.contador_fotogramas = 0

    def debe_procesar(self):
        self.contador_fotogramas += 1
        return self.contador_fotogramas % self.procesar_cada_n_fotogramas == 0
