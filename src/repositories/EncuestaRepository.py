class EncuestaRepository:
    def __init__(self):
        pass
    # Métodos stub para evitar ImportError
    def save(self, poll):
        pass
    def get(self, poll_id):
        pass
    def get_all_active(self):
        return []
    def has_voted(self, poll_id, username):
        return False
    def add_vote(self, poll_id, username, opcion):
        pass
    def set_status(self, poll_id, estado):
        pass
    def get_results(self, poll_id):
        return {}
    def save_result(self, poll_id, result):
        pass
    def get_votes(self, poll_id):
        return {}