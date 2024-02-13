from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar


OutputType = TypeVar("OutputType")


class Input(Generic[OutputType], metaclass=ABCMeta):
    @abstractmethod
    def load(self, path: str) -> OutputType:
        pass
