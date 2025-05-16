# Estrategias para desempate y presentación de resultados.

class TieBreakerStrategy:
    def break_tie(self, options):
        pass

class AlphabeticalTieBreaker(TieBreakerStrategy):
    def break_tie(self, options):
        # Implementación pendiente
        pass

class RandomTieBreaker(TieBreakerStrategy):
    def break_tie(self, options):
        # Implementación pendiente
        pass

class OvertimeTieBreaker(TieBreakerStrategy):
    def break_tie(self, options):
        # Implementación pendiente
        pass

class ResultFormatStrategy:
    def format(self, results):
        pass

class TextResultFormat(ResultFormatStrategy):
    def format(self, results):
        # Implementación pendiente
        pass

class AsciiGraphResultFormat(ResultFormatStrategy):
    def format(self, results):
        # Implementación pendiente
        pass

class JsonResultFormat(ResultFormatStrategy):
    def format(self, results):
        # Implementación pendiente
        pass
