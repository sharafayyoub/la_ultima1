import uuid
import time

class Poll:
    def __init__(self, pregunta, opciones, duracion_segundos, tipo="simple"):
        self.id = str(uuid.uuid4())
        self.pregunta = pregunta
        self.opciones = list(opciones)
        self.duracion_segundos = duracion_segundos
        self.tipo = tipo
        self.timestamp_inicio = int(time.time())
        self.estado = "activa"

    def add_option(self, opcion):
        self.opciones.append(opcion)

    def cerrar(self):
        self.estado = "cerrada"
