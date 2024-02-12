from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar


InputType = TypeVar("InputType")


class Output(Generic[InputType], metaclass=ABCMeta):
    @abstractmethod
    def dump(self, input: InputType) -> None:
        pass
