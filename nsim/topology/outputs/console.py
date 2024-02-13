from nsim.output import ConsoleOutput

from ..models.edge import Edge
from ..models.leaf import Leaf
from ..models.node import Node
from ..models.topology import Topology


class ConsoleTopologyOutput(ConsoleOutput[Node]):
    def __print_edge(self, edge: Edge, depth: int = 0) -> None:
        e_bps = edge.get_bandwidth()
        e_bandwidth = (
            f"{(e_bps / 10**6):.0f} Mbps"
            if e_bps < 10**9
            else f"{(e_bps / 10**9):.0f} Gbps"
        )

        e_dest = edge.get_destination()
        e_dest_id = e_dest.get_id()
        e_dest_type = e_dest.get_type().value

        self._print(e_dest_type, e_dest_id, f"({e_bandwidth})", depth)

    def __print_leaf(self, leaf: Leaf, depth: int = 0) -> None:
        l_type = leaf.get_type().value
        l_id = leaf.get_id()
        l_edges = leaf.get_edges()

        if len(l_edges) == 0:
            self._print(l_type, l_id, "has no edges.", depth)
        else:
            self._print(l_type, l_id, "has edges to:", depth)
            for edge in l_edges:
                self.__print_edge(edge, depth + 1)

    def __print_topology(self, topology: Topology, depth: int = 0) -> None:
        t_type = topology.__class__.__name__
        t_id = topology.get_id()
        t_nodes = topology.get_nodes()

        if len(t_nodes) == 0:
            self._print(t_type, t_id, "has no nodes.", depth)
        else:
            self._print(t_type, t_id, "has nodes:", depth)
            for node in t_nodes:
                self.__print_node(node, depth + 1)

    def __print_node(self, node: Node, depth: int = 0) -> None:
        if isinstance(node, Leaf):
            self.__print_leaf(node, depth)
        elif isinstance(node, Topology):
            self.__print_topology(node, depth)

    def run(self, node: Node) -> None:
        self.__print_node(node)
