from abc import ABC, abstractmethod


class Observador(ABC):

    @abstractmethod
    def atualizar(self, *args, **kwargs):
        ...


class Observavel(ABC):

    def __init__(self):
        self.observadores = []

    def observar(self, observador):
        self.observadores.append(observador)

    def parar_observar(self, observador):
        self.observadores.remove(observador)

    def notificar(self, *args, **kwargs):
        for observador in self.observadores:
            observador.atualizar(*args, **kwargs)
