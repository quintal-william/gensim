from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Generic, TypeVar
from xml.etree import ElementTree
from .topology.models.node import Node
from .topology.models.leaf import Leaf

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
    INET = "inet"


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

class OmnestOutput(Output[Node]):
    def _print(self, line: str = "", depth = 0) -> None:
        whitespace = "  " * depth
        console = Console(highlight=False)
        console.print(f"{whitespace}{line}", highlight=False)
    
    def _print_ini(self, leaves: list[Leaf]) -> Node:
        self._print("--- START INI FILE ---")
        self._print("[General]")
        self._print("network = Nsim")
        self._print_ini_leaves(leaves)
        self._print("--- END INI FILE ---")

    def _print_ned(self, leaves: list[Leaf]) -> None:
        self._print("--- START NED FILE ---")
        self._print("package nsim.simulations;")
        
        self._print()
        self._print_ned_imports(leaves)
        self._print()
        self._print("import nsim.NetworkAnalyzer;")
        self._print("import nsim.NetworkEntryPoint;")
        self._print("import nsim.NetworkExitPoint;")

        self._print()
        self._print("network Nsim {")
        self._print('@display("bgb=442,324");', 1)
        self._print('submodules:', 1)
        self._print('networkAnalyzer: NetworkAnalyzer {', 2)
        self._print('@display("p=222,261");', 3)
        self._print('}', 2)
        self._print('entry: NetworkEntryPoint {', 2)
        self._print('@display("p=389,195");', 3)
        self._print('}', 2)
        self._print('exit: NetworkExitPoint {', 2)
        self._print('@display("p=56,195");', 3)
        self._print('}', 2)
        self._print_ned_leaves(leaves)

        self._print()
        self._print('connections:', 1)
        self._print('networkAnalyzer.out --> entry.in;', 2)
        self._print('exit.out --> networkAnalyzer.in;', 2)
        self._print_ned_connections(leaves)

        self._print("}")
        self._print("--- END NED FILE ---")

        # TODO
        # import nsim.nodes.ConstantDelayNode;
        # import nsim.nodes.BandwidthNode;
        # import nsim.nodes.LatencyRateNode;
        # full: ConstantDelayNode {
        #     @display("p=222,83");
        #     delay = 20.4;
        # }
        # full: BandwidthNode {
        #     @display("p=222,83");
        #     bandwidth = 4.1;
        # }
        # full: LatencyRateNode {
        #     @display("p=222,83");
        #     latency = 5.6;
        #     rate = 3.1;
        # }
        # entry.out++ --> full.in;
        # full.out --> exit.in++;

    @abstractmethod
    def _print_ned_imports(self, leaves: list[Leaf]) -> None:
        pass

    @abstractmethod
    def _print_ned_leaves(self, leaves: list[Leaf]) -> None:
        pass

    @abstractmethod
    def _print_ned_connections(self, leaves: list[Leaf]) -> None:
        pass

    @abstractmethod
    def _print_ini_leaves(self, leaves: list[Leaf]) -> None:
        pass

    def run(self, node: Node) -> None:
        leaves = node.flatten()
        self._print_ned(leaves)
        self._print_ini(leaves)
