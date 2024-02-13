import json
from typing import NoReturn, TypedDict, TypeGuard, get_origin

from nsim.input import Input

from ...util import Json, fatal
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


Schema = Json | NodeSchema


class JsonTopologyInput(Input[Node]):
    def __parse_error(self, message: str) -> NoReturn:
        fatal(f"Error loading or parsing JSON data: {message}")

    def __validate_schema(self, data: Schema, schema: Json) -> bool:
        for k, v in schema.items():
            if k not in data:
                self.__parse_error(f"Key `{k}` not found in data: {data}")
            if (get_origin(v) is list and not isinstance(data.get(k), list)) or (
                get_origin(v) is not list and not isinstance(data.get(k), v)
            ):
                self.__parse_error(
                    f"Key `{k}` has invalid type. Requested: `{v}`, found: `{type(data.get(k))}`",
                )
        return True

    def __validate_node(self, data: Schema) -> TypeGuard[NodeSchema]:
        schema: Json = NodeSchema.__annotations__
        return self.__validate_schema(data, schema)

    def __validate_topology(self, data: Schema) -> TypeGuard[TopologySchema]:
        schema: Json = TopologySchema.__annotations__
        return self.__validate_schema(data, schema)

    def __validate_leaf(self, data: Schema) -> TypeGuard[LeafSchema]:
        schema: Json = LeafSchema.__annotations__
        return self.__validate_schema(data, schema)

    def __validate_edge(
        self,
        data: Json,
        leaves: dict[str, Leaf],
    ) -> TypeGuard[EdgeSchema]:
        schema: Json = EdgeSchema.__annotations__
        if self.__validate_schema(data, schema):
            if not data["source"] in leaves:
                self.__parse_error(f"Key `source` has invalid value in data: {data}")
            if not data["destination"] in leaves:
                self.__parse_error(
                    f"Key `destination` has invalid value in data: {data}",
                )
        return True

    def __parse_node(self, data: Json, leaves: dict[str, Leaf]) -> Node:
        if self.__validate_node(data):
            if data["type"] == "Topology":
                if self.__validate_topology(data):
                    topology = Topology(data["id"])
                    for node in data["nodes"]:
                        topology.add_node(self.__parse_node(node, leaves))
                    return topology

            if data["type"] == "Host" or data["type"] == "Switch":
                if self.__validate_leaf(data):
                    leaf = leaves[data["id"]]
                    for edge in data["edges"]:
                        self.__validate_edge(edge, leaves)
                        leaf.add_edge(leaves[edge["destination"]], edge["bandwidth"])
                    return leaf

        self.__parse_error(f"Key `type` has invalid value in node data: {data}")

    def __scan_leaves(
        self,
        data: Json,
        leaves: dict[str, Leaf] = dict(),
    ) -> dict[str, Leaf]:
        if self.__validate_node(data):
            if data["type"] == "Topology":
                if self.__validate_topology(data):
                    for node in data["nodes"]:
                        leaves = self.__scan_leaves(node, leaves)
            else:
                leaves[data["id"]] = Leaf(data["id"], leaf_type_from_str(data["type"]))
        return leaves

    def run(self, file_path: str) -> Node:
        try:
            with open(file_path) as file:
                data: Json = json.load(file)
        except Exception as e:
            self.__parse_error(str(e))

        leaves = self.__scan_leaves(data)
        node = self.__parse_node(data, leaves)
        return node
