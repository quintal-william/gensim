from nsim.generator import Generator

from ..models.leaf import Leaf, LeafType
from ..models.node import Node
from ..models.topology import Topology


class StarTopologyGenerator(Generator[Node]):
    """
    Generates a topology in which all hosts are connected the same switch at a rate according to some connectedness parameter c
    """

    def gen(self, generator_options: str | None) -> Node:
        name = self._get_input_name(generator_options)
        number_of_nodes = self._get_input_topology_number_of_nodes(generator_options)
        connectivity = self._get_input_topology_connectivity(generator_options)

        topology = Topology(name, number_of_nodes, connectivity)
        center = Leaf(f"{name}-center", LeafType.SWITCH)
        for node in topology.get_nodes():
            topology.connect(center, node)
        topology.add_node(center)

        return topology
