from nsim.generator import Generator

from .mesh import MeshTopologyGenerator
from .star import StarTopologyGenerator
from ..models.node import Node


topology_generators: dict[str, Generator[Node]] = {
    "mesh": MeshTopologyGenerator(),
    "star": StarTopologyGenerator(),
}
