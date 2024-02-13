from __future__ import annotations

from enum import Enum

from .edge import Edge
from .node import Node
from ...util import fatal


class LeafType(Enum):
    HOST = "Host"
    SWITCH = "Switch"


def leaf_type_from_str(s: str) -> LeafType:
    if s.lower() == "host":
        return LeafType.HOST
    if s.lower() == "switch":
        return LeafType.SWITCH
    fatal(f'String "{s}" could not be parsed to LeafType')


class Leaf(Node):
    """
    Represents the smallest possible unit in a network (e.g. Host, Switch)
    """

    __edges: list[Edge]
    __type: LeafType

    def __init__(self, id: str, type: LeafType) -> None:
        super().__init__(id)
        self.__type = type
        self.__edges = []

    def flatten(self) -> list[Leaf]:
        return [self]

    def add_edge(self, destination: Leaf, bandwidth: int) -> None:
        edge = Edge(
            source=self,
            destination=destination,
            bandwidth=bandwidth,
        )
        self.__edges.append(edge)

    def get_edges(self) -> list[Edge]:
        return self.__edges.copy()

    def get_type(self) -> LeafType:
        return self.__type
