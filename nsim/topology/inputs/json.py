from typing import TypedDict, TypeGuard, cast

from nsim.input import JsonInput

from ...util import Json
from ..models.leaf import Leaf, leaf_type_from_str
from ..models.node import Node
from ..models.topology import Topology


class NodeSchema(TypedDict):
    type: str
    id: str


class TopologySchema(NodeSchema):
    nodes: list[Json]


class LeafSchema(NodeSchema):
    edges: list[Json]


class EdgeSchema(NodeSchema):
    source: str
    destination: str
    bandwidth: int


class JsonTopologyInput(JsonInput[Node]):
    def __validate_node(self, data: Json) -> TypeGuard[NodeSchema]:
        schema: Json = NodeSchema.__annotations__
        return self._validate_schema(data, schema)

    def __validate_topology(self, data: Json) -> TypeGuard[TopologySchema]:
        schema: Json = TopologySchema.__annotations__
        return self._validate_schema(data, schema)

    def __validate_leaf(self, data: Json) -> TypeGuard[LeafSchema]:
        schema: Json = LeafSchema.__annotations__
        return self._validate_schema(data, schema)

    def __validate_edge(
        self,
        data: Json,
        leaves: dict[str, Leaf],
    ) -> TypeGuard[EdgeSchema]:
        schema: Json = EdgeSchema.__annotations__
        if self._validate_schema(data, schema):
            if not data["source"] in leaves:
                self._parse_error(f"Key `source` has invalid value in data: {data}")
            if not data["destination"] in leaves:
                self._parse_error(
                    f"Key `destination` has invalid value in data: {data}",
                )
        return True

    def __parse_node(self, data: Json, leaves: dict[str, Leaf]) -> Node:
        if self.__validate_node(data):
            if data["type"] == "Topology":
                topology_data = cast(Json, data)
                if self.__validate_topology(topology_data):
                    topology = Topology(topology_data["id"])
                    for node in topology_data["nodes"]:
                        topology.add_node(self.__parse_node(node, leaves))
                    return topology

            if data["type"] == "Host" or data["type"] == "Switch":
                leaf_data = cast(Json, data)
                if self.__validate_leaf(leaf_data):
                    leaf = leaves[leaf_data["id"]]
                    for edge in leaf_data["edges"]:
                        self.__validate_edge(edge, leaves)
                        leaf.add_edge(leaves[edge["destination"]], edge["bandwidth"])
                    return leaf

        self._parse_error(f"Key `type` has invalid value in node data: {data}")

    def __scan_leaves(
        self,
        data: Json,
        leaves: dict[str, Leaf] = dict(),
    ) -> dict[str, Leaf]:
        if self.__validate_node(data):
            if data["type"] == "Topology":
                topology_data = cast(Json, data)
                if self.__validate_topology(topology_data):
                    for node in topology_data["nodes"]:
                        leaves = self.__scan_leaves(node, leaves)
            else:
                leaves[data["id"]] = Leaf(data["id"], leaf_type_from_str(data["type"]))
        return leaves

    def run(self, data: Json) -> Node:
        leaves = self.__scan_leaves(data)
        node = self.__parse_node(data, leaves)
        return node
