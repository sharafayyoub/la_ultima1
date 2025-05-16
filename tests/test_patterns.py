import pytest
from src.patterns.Observer import Observable, Observer
from src.patterns.Factory import PollFactory
from src.patterns.Strategy import AlphabeticalTieBreaker, RandomTieBreaker

# Observer pattern test
class DummyObserver(Observer):
    def __init__(self):
        self.events = []
    def update(self, event, data):
        self.events.append((event, data))

def test_observer_notified_on_close():
    class DummyPollService(Observable):
        def close_poll(self):
            self.notify_observers("poll_closed", {"poll_id": "123"})
    obs = DummyObserver()
    service = DummyPollService()
    service.add_observer(obs)
    service.close_poll()
    assert obs.events and obs.events[0][0] == "poll_closed"

# Factory pattern test
class SimplePoll: pass
class MultiplePoll: pass

class CustomPollFactory(PollFactory):
    def create_poll(self, poll_type, *args, **kwargs):
        if poll_type == "simple":
            return SimplePoll()
        elif poll_type == "multiple":
            return MultiplePoll()
        else:
            raise ValueError("Tipo desconocido")

def test_factory_creates_correct_type():
    factory = CustomPollFactory()
    assert isinstance(factory.create_poll("simple"), SimplePoll)
    assert isinstance(factory.create_poll("multiple"), MultiplePoll)
    with pytest.raises(ValueError):
        factory.create_poll("otro")

# Strategy pattern test
def test_tiebreaker_strategies():
    empate = ["B", "A"]
    alpha = AlphabeticalTieBreaker()
    rand = RandomTieBreaker()
    # Alfabético siempre da "A"
    assert alpha.break_tie(empate) == "A"
    # Aleatorio puede ser cualquiera, forzamos resultado para test
    import random
    random.seed(0)
    ganador = rand.break_tie(empate)
    assert ganador in empate
