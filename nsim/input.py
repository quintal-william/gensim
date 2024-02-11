from abc import ABCMeta, abstractmethod


class Input(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def load(path: str) -> None:
        pass
