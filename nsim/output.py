from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar


InputType = TypeVar("InputType")


class Output(Generic[InputType], metaclass=ABCMeta):
    def run_super(self, input: InputType) -> None:
        self.run(input)

    @abstractmethod
    def run(self, input: InputType) -> None:
        pass
