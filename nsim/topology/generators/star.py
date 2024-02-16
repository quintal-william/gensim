from nsim.generator import Generator

from ..models.leaf import Leaf, LeafType
from ..models.node import Node
from ..models.topology import Topology


class StarTopologyGenerator(Generator[Node]):
    """
    Generates a topology in which all hosts are connected the same switch at a rate according to some connectedness parameter c
    """

    def run(self) -> Node:
        name = self._get_input_name()
        number_of_nodes = self._get_input_number_of_nodes()
        connectivity = self._get_input_connectivity()

        topology = Topology(name)
        center = Leaf(f"{name}_center", LeafType.SWITCH)
        topology.add_node(center)
        for i in range(number_of_nodes):
            leaf = Leaf(f"{name}_{i}", LeafType.HOST)
            center.connect(leaf, connectivity)
            topology.add_node(leaf)

        return topology
