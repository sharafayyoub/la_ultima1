# Definición base del patrón Observer para notificaciones de eventos (como cierre de encuesta).

class Observer:
    def update(self, event, data):
        pass

class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, event, data=None):
        for observer in self._observers:
            observer.update(event, data)
