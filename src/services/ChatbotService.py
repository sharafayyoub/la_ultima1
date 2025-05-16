from transformers import pipeline, Conversation
from src.services.PollService import PollService

class ChatbotService:
    def __init__(self):
        self.chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")
        self.histories = {}  # opcional: historial por usuario
        self.poll_service = PollService()

    def ask(self, username: str, message: str) -> str:
        # Palabras clave para contexto de encuestas
        keywords = [
            "quién va ganando", "quien va ganando", "quién lidera", "quien lidera",
            "cuánto falta", "cuanto falta", "resultado", "resultados", "votación", "encuesta"
        ]
        msg_lower = message.lower()
        if any(k in msg_lower for k in keywords):
            # Buscar encuesta activa
            polls = self.poll_service.poll_repo.get_all_active()
            if not polls:
                return "No hay encuestas activas en este momento."
            poll = polls[0]  # Tomar la primera activa
            if "quién va ganando" in msg_lower or "quien va ganando" in msg_lower or "quién lidera" in msg_lower or "quien lidera" in msg_lower:
                results = self.poll_service.get_partial_results(poll["id"])
                if not results:
                    return "Aún no hay votos registrados."
                max_votes = max([v["count"] for v in results.values()])
                ganadores = [op for op, v in results.items() if v["count"] == max_votes]
                if len(ganadores) == 1:
                    return f"La opción que va ganando es: {ganadores[0]} con {max_votes} votos."
                else:
                    return f"Hay empate entre: {', '.join(ganadores)} con {max_votes} votos cada uno."
            if "cuánto falta" in msg_lower or "cuanto falta" in msg_lower:
                now = int(__import__('time').time())
                restante = poll["timestamp_inicio"] + poll["duracion_segundos"] - now
                if restante > 0:
                    return f"Faltan {restante} segundos para que termine la encuesta."
                else:
                    return "La encuesta está por finalizar o ya finalizó."
            if "resultado" in msg_lower or "resultados" in msg_lower:
                results = self.poll_service.get_partial_results(poll["id"])
                if not results:
                    return "Aún no hay votos registrados."
                res_str = "Resultados parciales:\n"
                for op, v in results.items():
                    res_str += f"{op}: {v['count']} votos ({v['percent']:.1f}%)\n"
                return res_str.strip()
            return "¿Sobre qué aspecto de la encuesta quieres saber?"
        # Si no es sobre encuestas, usar IA
        if username not in self.histories:
            self.histories[username] = Conversation(message)
        else:
            self.histories[username].add_user_input(message)
        response = self.chatbot(self.histories[username])
        return str(response)
