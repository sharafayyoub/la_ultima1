import uuid
import time
from src.repositories.EncuestaRepository import EncuestaRepository
from src.services.NFTService import NFTService
from src.patterns.Observer import Observable
from src.patterns.Strategy import TieBreakerStrategy

class PollService(Observable):
    def __init__(self):
        super().__init__()
        self.poll_repo = EncuestaRepository()
        self.nft_service = NFTService()

    def _auto_close_polls(self):
        now = int(time.time())
        polls = self.poll_repo.get_all_active()
        for poll in polls:
            if now >= poll["timestamp_inicio"] + poll["duracion_segundos"]:
                self.close_poll(poll["id"])

    def create_poll(self, pregunta: str, opciones: list, duracion_segundos: int, tipo: str = "simple"):
        self._auto_close_polls()
        poll_id = str(uuid.uuid4())
        timestamp_inicio = int(time.time())
        poll = {
            "id": poll_id,
            "pregunta": pregunta,
            "opciones": opciones,
            "duracion_segundos": duracion_segundos,
            "tipo": tipo,
            "timestamp_inicio": timestamp_inicio,
            "estado": "activa"
        }
        self.poll_repo.save(poll)
        return poll_id

    def vote(self, poll_id: str, username: str, opcion):
        self._auto_close_polls()
        poll = self.poll_repo.get(poll_id)
        if not poll or poll["estado"] != "activa":
            return False  # Encuesta no existe o no está activa

        # Verificar si el usuario ya votó
        if self.poll_repo.has_voted(poll_id, username):
            return False

        # Registrar el voto
        self.poll_repo.add_vote(poll_id, username, opcion)

        # Generar token NFT
        self.nft_service.generate_token(username, poll_id, opcion, int(time.time()))
        return True

    def close_poll(self, poll_id: str):
        poll = self.poll_repo.get(poll_id)
        if not poll or poll["estado"] != "activa":
            return False
        self.poll_repo.set_status(poll_id, "cerrada")
        result = self.poll_repo.get_results(poll_id)
        self.notify_observers("poll_closed", {"poll_id": poll_id, "result": result})
        self.poll_repo.save_result(poll_id, result)
        return True

    def close_poll_manual(self, poll_id: str):
        # Permite cierre manual anticipado
        return self.close_poll(poll_id)

    def get_partial_results(self, poll_id: str):
        poll = self.poll_repo.get(poll_id)
        if not poll:
            return None
        votes = self.poll_repo.get_votes(poll_id)
        total = sum(votes.values())
        results = {}
        for opcion, count in votes.items():
            percent = (count / total * 100) if total > 0 else 0
            results[opcion] = {"count": count, "percent": percent}
        return results

    def get_final_results(self, poll_id: str, tiebreaker: TieBreakerStrategy = None):
        poll = self.poll_repo.get(poll_id)
        if not poll or poll["estado"] != "cerrada":
            return None
        votes = self.poll_repo.get_votes(poll_id)
        total = sum(votes.values())
        results = {}
        for opcion, count in votes.items():
            percent = (count / total * 100) if total > 0 else 0
            results[opcion] = {"count": count, "percent": percent}
        # Desempate si corresponde
        if tiebreaker:
            max_votes = max(votes.values(), default=0)
            empates = [op for op, c in votes.items() if c == max_votes]
            if len(empates) > 1:
                ganador = tiebreaker.break_tie(empates)
                results["ganador"] = ganador
        return results
