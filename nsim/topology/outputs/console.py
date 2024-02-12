from rich.console import Console

from nsim.output import Output

from ..models.edge import Edge
from ..models.leaf import Leaf
from ..models.node import Node
from ..models.topology import Topology


class ConsoleTopologyOutput(Output[Node]):
    @staticmethod
    def __print(item_type: str, item_id: str, message: str, depth: int) -> None:
        print_whitespace = "  " * depth
        print_type = rf"[cyan]\[{item_type}][/cyan]"
        print_id = f"[yellow]{item_id}[/yellow]"
        console = Console(highlight=False)
        console.print(f"{print_whitespace}- {print_type} {print_id} {message}", highlight=False)

    @staticmethod
    def __print_edge(edge: Edge, depth: int = 0) -> None:
        e_bps = edge.get_bandwidth()
        e_bandwidth = (
            f"{(e_bps / 10**6):.0f} Mbps"
            if e_bps < 10**9
            else f"{(e_bps / 10**9):.0f} Gbps"
        )

        e_dest = edge.get_destination()
        e_dest_id = e_dest.get_id()
        e_dest_type = e_dest.get_type().value

        ConsoleTopologyOutput.__print(e_dest_type, e_dest_id, f"({e_bandwidth})", depth)

    @staticmethod
    def __print_leaf(leaf: Leaf, depth: int = 0) -> None:
        l_type = leaf.get_type().value
        l_id = leaf.get_id()
        l_edges = leaf.get_edges()

        if len(l_edges) == 0:
            ConsoleTopologyOutput.__print(l_type, l_id, "has no edges.", depth)
        else:
            ConsoleTopologyOutput.__print(l_type, l_id, "has edges to:", depth)
            for edge in l_edges:
                ConsoleTopologyOutput.__print_edge(edge, depth + 1)

    @staticmethod
    def __print_topology(topology: Topology, depth: int = 0) -> None:
        t_type = topology.__class__.__name__
        t_id = topology.get_id()
        t_nodes = topology.get_nodes()

        if len(t_nodes) == 0:
            ConsoleTopologyOutput.__print(t_type, t_id, "has no nodes.", depth)
        else:
            ConsoleTopologyOutput.__print(t_type, t_id, "has nodes:", depth)
            for node in t_nodes:
                ConsoleTopologyOutput.__print_node(node, depth + 1)

    @staticmethod
    def __print_node(node: Node, depth: int = 0) -> None:
        if isinstance(node, Leaf):
            ConsoleTopologyOutput.__print_leaf(node, depth)
        elif isinstance(node, Topology):
            ConsoleTopologyOutput.__print_topology(node, depth)

    @staticmethod
    def dump(node: Node) -> None:
        ConsoleTopologyOutput.__print_node(node)
