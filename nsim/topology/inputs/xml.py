import xml.etree.ElementTree as ElementTree
from typing import Callable, NoReturn

from nsim.input import Input

from ...util import Json, fatal
from ..models.leaf import Leaf, LeafType, leaf_type_from_str
from ..models.node import Node
from ..models.topology import Topology


Schema = dict[str, Callable[[str], int | str | LeafType]]


class XmlTopologyInput(Input[Node]):
    def __parse_error(self, message: str) -> NoReturn:
        fatal(f"Error loading or parsing XML data: {message}")

    def __parse_attributes(
        self,
        element: ElementTree.Element,
        schema: Schema,
    ) -> Json:
        raw_attributes = element.attrib
        attributes: Json = {}
        for k, v in schema.items():
            if k not in raw_attributes:
                self.__parse_error(
                    f"Key `{k}` not found in attributes: {raw_attributes}",
                )

            try:
                attributes[k] = v(raw_attributes[k])
            except:
                self.__parse_error(
                    f"Key `{k}` has invalid type. Requested: `{v}`, found: `{raw_attributes[k]}`",
                )
        return attributes

    def __parse_topology(
        self,
        element: ElementTree.Element,
        leaves: dict[str, Leaf],
    ) -> Topology:
        attr = self.__parse_attributes(element, {"id": str})
        topology = Topology(attr["id"])
        for node_element in element:
            topology.add_node(self.__parse_node(node_element, leaves))
        return topology

    def __parse_leaf(
        self,
        element: ElementTree.Element,
        leaves: dict[str, Leaf],
    ) -> Leaf:
        attr = self.__parse_attributes(element, {"id": str})
        leaf = Leaf(attr["id"], leaf_type_from_str(element.tag))
        for edge_element in element.findall("edge"):
            e_schema: Schema = {"source": str, "destination": str, "bandwidth": int}
            e_attr = self.__parse_attributes(edge_element, e_schema)

            if not (e_attr["source"] == attr["id"]):  # type: ignore [misc]
                self.__parse_error(f"Mismatched source: {e_attr['source']}")
            if e_attr["destination"] not in leaves:
                self.__parse_error(f"Unknown destination: {e_attr['destination']}")

            leaf.add_edge(leaves[e_attr["destination"]], e_attr["bandwidth"])
        return leaf

    def __parse_node(
        self,
        element: ElementTree.Element,
        leaves: dict[str, Leaf],
    ) -> Node:
        node_type = element.tag
        if node_type == "topology":
            return self.__parse_topology(element, leaves)
        if node_type == "host" or node_type == "switch":
            return self.__parse_leaf(element, leaves)
        self.__parse_error(f"Tag unknown {node_type}")

    def __scan_leaves(
        self,
        element: ElementTree.Element,
        leaves: dict[str, Leaf] = dict(),
    ) -> dict[str, Leaf]:
        node_type = element.tag
        if node_type == "topology":
            for node_element in element:
                leaves = self.__scan_leaves(node_element, leaves)
        if node_type == "host" or node_type == "switch":
            attr = self.__parse_attributes(element, {"id": str})
            leaves[attr["id"]] = Leaf(attr["id"], leaf_type_from_str(node_type))
        return leaves

    def run(self, file_path: str) -> Node:
        try:
            tree = ElementTree.parse(file_path)
        except Exception as e:
            self.__parse_error(str(e))

        root: ElementTree.Element = tree.getroot()
        leaves = self.__scan_leaves(root)
        node = self.__parse_node(root, leaves)
        return node
