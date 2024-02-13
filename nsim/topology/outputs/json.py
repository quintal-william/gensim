import json

from nsim.output import Output

from ...util import Json
from ..models.edge import Edge
from ..models.leaf import Leaf
from ..models.node import Node
from ..models.topology import Topology


class JsonTopologyOutput(Output[Node]):
    def __make_item(self, item_type: str, item_id: str) -> Json:
        data: Json = {
            "type": item_type,
            "id": item_id,
        }
        return data

    def __make_edge_data(self, edge: Edge) -> Json:
        data = self.__make_item(edge.__class__.__name__, edge.get_id())
        data["source"] = edge.get_source().get_id()
        data["destination"] = edge.get_destination().get_id()
        data["bandwidth"] = edge.get_bandwidth()
        return data

    def __make_leaf_data(self, leaf: Leaf) -> Json:
        data = self.__make_item(leaf.get_type().value, leaf.get_id())
        edges_data: list[Json] = []
        data["edges"] = edges_data
        for edge in leaf.get_edges():
            data["edges"].append(self.__make_edge_data(edge))
        return data

    def __make_topology_data(self, topology: Topology) -> Json:
        data = self.__make_item(topology.__class__.__name__, topology.get_id())
        nodes_data: list[Json] = []
        data["nodes"] = nodes_data
        for node in topology.get_nodes():
            data["nodes"].append(self.__make_node_data(node))
        return data

    def __make_node_data(self, node: Node) -> Json:
        if isinstance(node, Leaf):
            return self.__make_leaf_data(node)
        if isinstance(node, Topology):
            return self.__make_topology_data(node)
        return self.__make_item(node.__class__.__name__, node.get_id())

    def run(self, node: Node) -> None:
        data = self.__make_node_data(node)
        print(json.dumps(data, indent=2))
