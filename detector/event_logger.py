import os


class RegistradorEventos:
    def __init__(self, directorio_base="eventos"):
        self.directorio_base = directorio_base
        os.makedirs(directorio_base, exist_ok=True)
