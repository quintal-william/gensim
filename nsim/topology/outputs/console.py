from rich import print

from nsim.output import Output

from ..models.edge import Edge
from ..models.leaf import Leaf
from ..models.node import Node
from ..models.topology import Topology


class ConsoleTopologyOutput(Output[Node]):
    @staticmethod
    def __print(item_type: str, item_id: str, message: str, depth: int) -> None:
        print_whitespace = "  " * depth
        print_type = fr"[cyan]\[{item_type}][/cyan]"
        print_id = f"[yellow]{item_id}[/yellow]"
        print(f"{print_whitespace}- {print_type} {print_id} {message}")

    @staticmethod
    def __print_edge(edge: Edge, depth: int = 0) -> None:
        e_id = edge.get_id()
        dest_id = edge.get_destination().get_id()

def convert_to_readable_bandwidth(bps):
    # Convert bps to Mbps and Gbps
    mbps = bps / 10**6
    gbps = bps / 10**9
    
    # Determine the most appropriate unit to display
    if bps < 10**9:  # Less than 1 Gbps, display in Mbps
        return f"{mbps:.2f} Mbps"
    else:  # 1 Gbps or more, display in Gbps
        return f"{gbps:.2f} Gbps"

# Example usage
bps_values = [10000000, 100000000, 1000000000, 10000000000, 25000000000, 40000000000, 100000000000]

# Convert and print each value
for bps in bps_values:
    readable_bandwidth = convert_to_readable_bandwidth(bps)
    print(f"{bps} bps is equivalent to {readable_bandwidth}")

        ConsoleTopologyOutput.__print(dest_id, e_id, f"({edge.get_bandwidth()}bps)", depth)

    @staticmethod
    def __print_leaf(leaf: Leaf, depth: int = 0) -> None:
        l_type = str(leaf.get_type())
        l_id = leaf.get_id()
        l_edges = leaf.get_edges()

        if len(l_edges) == 0:
            ConsoleTopologyOutput.__print(l_type, l_id, "has no edges.", depth)
        else:
            ConsoleTopologyOutput.__print(l_type, l_id, "has edges:", depth)
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
