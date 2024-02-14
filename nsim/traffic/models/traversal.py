from queue import Queue
from random import choice
from typing import cast

from .route import Route
from ...util import fatal
from ...topology.models.leaf import Leaf
from ...topology.models.node import Node


class Traversal:
    __leaves: list[Leaf]
    __reachable: dict[Leaf, set[Leaf]]
    __has_route: bool

    def __init__(self, node: Node) -> None:
        self.__leaves = node.flatten()
        self.__reachable = {}
        self.__has_route = False

        for leaf in self.__leaves:
            queue: Queue[Leaf] = Queue()
            queue.put(leaf)
            reachable: set[Leaf] = {leaf}

            while not queue.empty():
                for neighbour in queue.get().get_edges():
                    if neighbour.get_destination() not in reachable:
                        reachable.add(neighbour.get_destination())
                        queue.put(neighbour.get_destination())

            reachable.remove(leaf)
            self.__reachable[leaf] = reachable

        self.__has_route = any(self.__is_valid_source(leaf) for leaf in self.__leaves)

    def __is_valid_source(self, leaf: Leaf) -> bool:
        return len(self.__reachable[leaf]) > 0

    def get_random_route(self) -> Route:
        if not self.__has_route:
            fatal(f"Topology has no valid routes")

        def get_source() -> Leaf:
            source: Leaf | None = None
            while source == None or not self.__is_valid_source(cast(Leaf, source)):
                source = choice(self.__leaves)
            return cast(Leaf, source)

        source = get_source()
        destination = choice(list(self.__reachable[source]))
        return Route(source, destination)
