from ...topology.models.leaf import Leaf


class Route:
    __source: Leaf
    __destination: Leaf

    def __init__(self, source: Leaf, destination: Leaf) -> None:
        self.__source = source
        self.__destination = destination

    def get_source(self) -> Leaf:
        return self.__source

    def get_destination(self) -> Leaf:
        return self.__destination
