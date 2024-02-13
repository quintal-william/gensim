from nsim.generator import Generator

from ..models.node import Node
from ..models.topology import Topology


class MeshTopologyGenerator(Generator[Node]):
    """
    Generates a topology in which hosts are directly connected to one another at a rate according to some connectedness parameter c
    """

    def gen(self, generator_options: str | None) -> Node:
        name = self._get_input_name(generator_options)
        number_of_nodes = self._get_input_topology_number_of_nodes(generator_options)
        connectivity = self._get_input_topology_connectivity(generator_options)

        topology = Topology(name, number_of_nodes)
        nodes = topology.get_nodes()
        while len(nodes) > 0:
            node_a = nodes.pop()
            for node_b in nodes:
                topology.connect(node_a, node_b, connectivity)

        return topology
