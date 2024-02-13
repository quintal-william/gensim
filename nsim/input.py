from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar


OutputType = TypeVar("OutputType")


class Input(Generic[OutputType], metaclass=ABCMeta):
    def run_super(self, file_path: str) -> OutputType:
        return self.run(file_path)

    @abstractmethod
    def run(self, file_path: str) -> OutputType:
        pass
