from .leaf import Leaf
from .node import Node


class Topology(Node):
    """
    Data structure that holds nested structures of LeafNodes
    """

    __nodes: list[Node] = []

    def add_node(self, node: Node) -> None:
        self.__nodes.append(node)

    def get_nodes(self) -> list[Node]:
        return self.__nodes.copy()

    def flatten(self) -> list[Leaf]:
        leaf_nodes: list[Leaf] = []
        for node in self.__nodes:
            leaf_nodes.extend(node.flatten())
        return leaf_nodes
