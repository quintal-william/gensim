from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Generic, TypeVar
from xml.etree import ElementTree

from rich.console import Console

from .util import Json


TInputType = TypeVar("TInputType")


class Output(Generic[TInputType], metaclass=ABCMeta):
    def run_super(self, input: TInputType) -> None:
        self.run(input)

    @abstractmethod
    def run(self, input: TInputType) -> None:
        pass


class OutputType(str, Enum):
    CONSOLE = "console"
    JSON = "json"
    XML = "xml"
    OMNEST = "omnest"


class ConsoleOutput(Generic[TInputType], Output[TInputType]):
    def _print(
        self,
        item_type: str,
        item_id: str,
        message: str = "",
        depth: int = 0,
    ) -> None:
        print_whitespace = "  " * depth
        print_type = rf"[cyan]\[{item_type}][/]"
        print_id = f"[yellow]{item_id}[/]"
        console = Console(highlight=False)
        console.print(
            f"{print_whitespace}- {print_type} {print_id} {message}",
            highlight=False,
        )


class JsonOutput(Generic[TInputType], Output[TInputType]):
    def _make_item(self, item_type: str, item_id: str) -> Json:
        data: Json = {
            "type": item_type,
            "id": item_id,
        }
        return data


class XmlOutput(Generic[TInputType], Output[TInputType]):
    def _make_element(
        self,
        item_type: str,
        item_id: str,
        attributes: dict[str, str] | None = None,
    ) -> ElementTree.Element:
        attributes = attributes or {}
        attributes["id"] = item_id
        element = ElementTree.Element(item_type, attrib=attributes)
        return element
