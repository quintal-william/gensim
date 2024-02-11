from __future__ import annotations

from typing import TYPE_CHECKING

from ...model import Model


if TYPE_CHECKING:
    from .leaf import Leaf

class Edge(Model):
    '''
    Represents the connection between two Leafs
    '''

    __source: Leaf
    __destination: Leaf
    __bandwidth: int

    def __init__(self, source: Leaf, destination: Leaf, bandwidth: int) -> None:
        super().__init__(f"{source.get_id()}_{destination.get_id()}_{bandwidth}")
        self.__source = source
        self.__destination = destination
        self.__bandwidth = bandwidth

    def get_source(self) -> Leaf:
        return self.__source

    def get_destination(self) -> Leaf:
        return self.__destination

    def get_bandwidth(self) -> int:
        return self.__bandwidth
