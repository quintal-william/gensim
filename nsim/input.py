import json
import xml.etree.ElementTree as ElementTree
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Any, Generic, TypeVar, Callable, NoReturn, get_origin

from .util import Json, fatal


TInputType = TypeVar("TInputType")
TOutputType = TypeVar("TOutputType")

Schema = dict[str, Callable[[str], Any]]  # type: ignore [misc]


class Input(Generic[TInputType, TOutputType], metaclass=ABCMeta):
    @abstractmethod
    def run_super(self, file_path: str) -> TOutputType:
        pass

    @abstractmethod
    def run(self, data: TInputType) -> TOutputType:
        pass


class InputType(str, Enum):
    JSON = "json"
    XML = "xml"


class JsonInput(Generic[TOutputType], Input[Json, TOutputType]):
    def _parse_error(self, message: str) -> NoReturn:
        fatal(f"Error loading or parsing JSON data: {message}")

    def _validate_schema(self, data: Json, schema: Json) -> bool:
        for k, v in schema.items():
            if k not in data:
                self._parse_error(f"Key `{k}` not found in data: {data}")
            if (get_origin(v) is list and not isinstance(data.get(k), list)) or (
                get_origin(v) is not list and not isinstance(data.get(k), v)
            ):
                self._parse_error(
                    f"Key `{k}` has invalid type. Requested: `{v}`, found: `{type(data.get(k))}`",
                )
        return True

    def run_super(self, file_path: str) -> TOutputType:
        try:
            with open(file_path) as file:
                data: Json = json.load(file)
        except Exception as e:
            self._parse_error(str(e))
        return self.run(data)


class XmlInput(Generic[TOutputType], Input[ElementTree.Element, TOutputType]):
    def _parse_error(self, message: str) -> NoReturn:
        fatal(f"Error loading or parsing XML data: {message}")

    def _parse_attributes(
        self,
        element: ElementTree.Element,
        schema: Schema,
    ) -> Json:
        raw_attributes = element.attrib
        attributes: Json = {}
        for k, v in schema.items():
            if k not in raw_attributes:
                self._parse_error(
                    f"Key `{k}` not found in attributes: {raw_attributes}",
                )

            try:
                attributes[k] = v(raw_attributes[k])
            except:
                self._parse_error(
                    f"Key `{k}` has invalid type. Requested: `{v}`, found: `{raw_attributes[k]}`",
                )
        return attributes

    def run_super(self, file_path: str) -> TOutputType:
        try:
            tree = ElementTree.parse(file_path)
        except Exception as e:
            self._parse_error(str(e))
        root: ElementTree.Element = tree.getroot()
        return self.run(root)
