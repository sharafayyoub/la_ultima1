import pytest
import time
from src.services.PollService import PollService
from src.patterns.Strategy import AlphabeticalTieBreaker, RandomTieBreaker

class DummyRepo:
    def __init__(self):
        self.polls = {}
        self.votes = {}
        self.status = {}
        self.results = {}

    def save(self, poll):
        self.polls[poll["id"]] = poll
        self.status[poll["id"]] = poll["estado"]

    def get(self, poll_id):
        return self.polls.get(poll_id)

    def get_all_active(self):
        return [p for p in self.polls.values() if p["estado"] == "activa"]

    def has_voted(self, poll_id, username):
        return username in self.votes.get(poll_id, {})

    def add_vote(self, poll_id, username, opcion):
        if poll_id not in self.votes:
            self.votes[poll_id] = {}
        self.votes[poll_id][username] = opcion

    def get_votes(self, poll_id):
        votes = self.votes.get(poll_id, {})
        counts = {}
        for op in set(votes.values()):
            counts[op] = list(votes.values()).count(op)
        return counts

    def set_status(self, poll_id, estado):
        self.polls[poll_id]["estado"] = estado
        self.status[poll_id] = estado

    def get_results(self, poll_id):
        return self.get_votes(poll_id)

    def save_result(self, poll_id, result):
        self.results[poll_id] = result

class DummyNFTService:
    def mint_token(self, username, poll_id, opcion):
        pass

@pytest.fixture
def poll_service(monkeypatch):
    ps = PollService()
    ps.poll_repo = DummyRepo()
    ps.nft_service = DummyNFTService()
    return ps

def test_crear_encuesta_y_votar(poll_service):
    poll_id = poll_service.create_poll("¿Color favorito?", ["Rojo", "Azul"], 60)
    assert poll_id in poll_service.poll_repo.polls
    assert poll_service.vote(poll_id, "alice", "Rojo")
    assert poll_service.vote(poll_id, "bob", "Azul")
    results = poll_service.get_partial_results(poll_id)
    assert results["Rojo"]["count"] == 1
    assert results["Azul"]["count"] == 1

def test_voto_duplicado_rechazado(poll_service):
    poll_id = poll_service.create_poll("¿Pizza?", ["Sí", "No"], 60)
    assert poll_service.vote(poll_id, "alice", "Sí")
    assert not poll_service.vote(poll_id, "alice", "No")

def test_cierre_automatico(poll_service, monkeypatch):
    poll_id = poll_service.create_poll("¿Café?", ["Solo", "Con leche"], 1)
    # Simular tiempo pasado
    poll = poll_service.poll_repo.get(poll_id)
    poll["timestamp_inicio"] -= 2
    poll_service._auto_close_polls()
    assert poll_service.poll_repo.get(poll_id)["estado"] == "cerrada"

def test_desempate_alfabetico(poll_service):
    poll_id = poll_service.create_poll("¿Mascota?", ["Perro", "Gato"], 60)
    poll_service.vote(poll_id, "a", "Perro")
    poll_service.vote(poll_id, "b", "Gato")
    poll_service.close_poll(poll_id)
    tiebreaker = AlphabeticalTieBreaker()
    result = poll_service.get_final_results(poll_id, tiebreaker)
    assert result["ganador"] == "Gato"  # Alfabéticamente primero

def test_desempate_aleatorio(poll_service, monkeypatch):
    poll_id = poll_service.create_poll("¿Fruta?", ["Manzana", "Pera"], 60)
    poll_service.vote(poll_id, "a", "Manzana")
    poll_service.vote(poll_id, "b", "Pera")
    poll_service.close_poll(poll_id)
    tiebreaker = RandomTieBreaker()
    # Forzar resultado para testeo determinista
    monkeypatch.setattr("random.choice", lambda opts: "Pera")
    result = poll_service.get_final_results(poll_id, tiebreaker)
    assert result["ganador"] == "Pera"
