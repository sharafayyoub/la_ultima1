import pytest
from src.models.Poll import Poll

def test_creacion_encuesta():
    poll = Poll("¿Te gusta Python?", ["Sí", "No"], 60, "simple")
    assert poll.pregunta == "¿Te gusta Python?"
    assert poll.opciones == ["Sí", "No"]
    assert poll.estado == "activa"

def test_añadir_opcion():
    poll = Poll("¿Lenguaje favorito?", ["Python"], 60, "simple")
    poll.add_option("JavaScript")
    assert "JavaScript" in poll.opciones

def test_cerrar_encuesta():
    poll = Poll("¿Café o té?", ["Café", "Té"], 60, "simple")
    poll.cerrar()
    assert poll.estado == "cerrada"
