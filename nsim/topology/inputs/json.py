import json
from typing import NoReturn, TypedDict, TypeGuard

import typer

from nsim.input import Input

from ...types import Json
from ...logger import logger
from ..models.leaf import Leaf, LeafType
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


class JsonTopologyInput(Input[Node]):
    def __parse_error(self, message: str) -> NoReturn:
        logger.error(f"Error loading or parsing JSON data: {message}")
        raise typer.Exit()

    def __validate_schema(self, data: Json, schema: Json) -> bool:
        for k, v in schema.items():
            if k not in data:
                self.__parse_error(f"Key `{k}` not found in data: {data}")
            if not isinstance(data[k], v):
                self.__parse_error(
                    f"Key `{k}` has invalid type. Requested: `{v}`, found: `{type(data[k])}`",
                )
        return True

    def __validate_node(self, data: Json) -> TypeGuard[NodeSchema]:
        schema: Json = NodeSchema.__annotations__
        return self.__validate_schema(data, schema)

    def __validate_topology(self, data: Json) -> TypeGuard[TopologySchema]:
        schema: Json = TopologySchema.__annotations__
        return self.__validate_schema(data, schema)

    def __validate_leaf(self, data: Json) -> TypeGuard[LeafSchema]:
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
                # TODO
                if self.__validate_topology(data):  # type: ignore [arg-type]
                    topology = Topology(data["id"])
                    for node in data["nodes"]:
                        topology.add_node(self.__parse_node(node, leaves))
                    return topology

            if data["type"] == "Host" or data["type"] == "Switch":
                # TODO
                if self.__validate_leaf(data):  # type: ignore [arg-type]
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
                # TODO
                if self.__validate_topology(data):  # type: ignore [arg-type]
                    for node in data["nodes"]:
                        leaves = self.__scan_leaves(node, leaves)
            elif data["type"] == "Host":
                leaves[data["id"]] = Leaf(data["id"], LeafType.HOST)
            elif data["type"] == "Switch":
                leaves[data["id"]] = Leaf(data["id"], LeafType.SWITCH)
        return leaves

    def load(self, file_path: str) -> Node:
        try:
            with open(file_path) as file:
                data: Json = json.load(file)
        except Exception as e:
            self.__parse_error(str(e))

        leaves = self.__scan_leaves(data)
        node = self.__parse_node(data, leaves)
        return node
