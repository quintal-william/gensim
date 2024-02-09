from abc import ABCMeta, abstractmethod

class Generator(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def gen() -> None:
        pass
