import random

from .leaf import Leaf, LeafType
from .node import Node
from ...types import Nodes, Connectivity


class Topology(Node):
    """
    Data structure that holds nested structures of LeafNodes
    """

    __connectivity: Connectivity
    __nodes: list[Node]

    def __init__(self, name: str, nodes: Nodes, connectivity: Connectivity) -> None:
        super().__init__(name)

        self.__connectivity = connectivity
        self.__nodes = []

        if isinstance(nodes, int):
            for i in range(nodes):
                leaf_node = Leaf(f"{name}-{i}", LeafType.HOST)
                self.add_node(leaf_node)
        else:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node: Node) -> None:
        self.__nodes.append(node)

    def get_nodes(self) -> list[Node]:
        return self.__nodes.copy()

    def flatten(self) -> list[Leaf]:
        leaf_nodes: list[Leaf] = []
        for node in self.__nodes:
            leaf_nodes.extend(node.flatten())
        return leaf_nodes

    def connect(self, node_a: Node, node_b: Node, bandwidth: int | None = None) -> None:
        if bandwidth == None:
            bandwidths = [
                10000000,  # 10BASE-T, 10 Mbps, rarely used in modern settings
                100000000,  # 100BASE-TX, 100 Mbps, in use for some home networks
                1000000000,  # 1000BASE-T, 1 Gbps, common in modern home networks
                10000000000,  # 10GBASE-T, 10 Gbps, used in enterprise networks and data centers
                25000000000,  # 25GBASE-T, 25 Gbps, increasingly adopted in data centers
                40000000000,  # 40GBASE-T, 40 Gbps, used in high-speed backbones of data center networks
                100000000000,  # 100GBASE-T, 100 Gbps, used in large data centers and internet backbones
            ]
            bandwidth = random.choice(bandwidths)

        nodes_a = node_a.flatten()
        nodes_b = node_b.flatten()

        for a in nodes_a:
            for b in nodes_b:
                if self.__connectivity > random.random():
                    bandwidth = random.choice(bandwidths)
                    a.add_edge(b, bandwidth)
                    b.add_edge(a, bandwidth)
