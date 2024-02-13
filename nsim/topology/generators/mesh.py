from nsim.generator import Generator

from ..models.leaf import Leaf, LeafType
from ..models.node import Node
from ..models.topology import Topology


class MeshTopologyGenerator(Generator[Node]):
    """
    Generates a topology in which hosts are directly connected to one another at a rate according to some connectedness parameter c
    """

    def run(self) -> Node:
        name = self._get_input_name()
        number_of_nodes = self._get_input_number_of_nodes()
        connectivity = self._get_input_connectivity()

        topology = Topology(name)
        for i in range(number_of_nodes):
            leaf = Leaf(f"{name}-{i}", LeafType.HOST)
            for node in topology.get_nodes():
                leaf.connect(node, connectivity)
            topology.add_node(leaf)

        return topology
