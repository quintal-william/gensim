from nsim.generator import Generator

from ...logger import logger
from ..models.node import Node
from ..models.topology import Topology


class MeshTopologyGenerator(Generator[Node]):
    """
    Generates a topology in which hosts are directly connected to one another at a rate according to some connectedness parameter c
    """

    @staticmethod
    def gen() -> Node:
        name = Generator._get_input(
            "the network name",
            "a string with length > 0 and < 30",
            str,
            lambda s: len(s) > 0 and len(s) < 30,
        )
        logger.debug(f"Set name to {name}")

        number_of_nodes = Generator._get_input(
            "the number of nodes",
            "a valid integer with value >= 0 and < 100,000",
            int,
            lambda n: n >= 0 and n < 100000,
        )
        logger.debug(f"Set number_of_nodes to {number_of_nodes}")

        connectivity = Generator._get_input(
            "the connectivity",
            "a valid float with value >= 0 and <= 1",
            float,
            lambda n: n >= 0 and n <= 1,
        )
        logger.debug(f"Set connectivity to {connectivity}")

        topology = Topology(name, number_of_nodes, connectivity)
        queue = topology.get_nodes()
        while len(queue) > 0:
            node_a = queue.pop()
            for node_b in queue:
                topology.connect(node_a, node_b)

        return topology
