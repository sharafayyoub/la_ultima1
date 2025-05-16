import pytest
from src.services.ChatbotService import ChatbotService

class DummyPollService:
    class DummyPollRepo:
        def get_all_active(self):
            return [{"id": "poll1", "pregunta": "¿Color?", "timestamp_inicio": 0, "duracion_segundos": 60}]
    def __init__(self):
        self.poll_repo = self.DummyPollRepo()
    def get_partial_results(self, poll_id):
        return {"Rojo": {"count": 2, "percent": 66.7}, "Azul": {"count": 1, "percent": 33.3}}

@pytest.fixture
def chatbot_service(monkeypatch):
    cs = ChatbotService()
    cs.poll_service = DummyPollService()
    # Mock pipeline IA para preguntas libres
    cs.chatbot = lambda conv: "Respuesta IA"
    return cs

def test_respuesta_quien_va_ganando(chatbot_service):
    resp = chatbot_service.ask("alice", "¿Quién va ganando?")
    assert "Rojo" in resp or "empate" in resp or "opción" in resp

def test_respuesta_cuanto_falta(chatbot_service):
    resp = chatbot_service.ask("alice", "¿Cuánto falta?")
    assert "Faltan" in resp or "finalizó" in resp

def test_respuesta_resultados(chatbot_service):
    resp = chatbot_service.ask("alice", "resultados")
    assert "Resultados parciales" in resp or "votos" in resp

def test_respuesta_libre_usa_ia(chatbot_service):
    resp = chatbot_service.ask("alice", "¿Cuál es el sentido de la vida?")
    assert resp == "Respuesta IA"
