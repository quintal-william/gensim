from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar


InputType = TypeVar("InputType")


class Output(Generic[InputType], metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def dump(input: InputType) -> None:
        pass
