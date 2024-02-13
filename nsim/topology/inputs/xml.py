import xml.etree.ElementTree as ElementTree

from nsim.input import Schema, XmlInput

from ..models.leaf import Leaf, leaf_type_from_str
from ..models.node import Node
from ..models.topology import Topology


class XmlTopologyInput(XmlInput[Node]):
    def __parse_topology(
        self,
        element: ElementTree.Element,
        leaves: dict[str, Leaf],
    ) -> Topology:
        attr = self._parse_attributes(element, {"id": str})
        topology = Topology(attr["id"])
        for node_element in element:
            topology.add_node(self.__parse_node(node_element, leaves))
        return topology

    def __parse_leaf(
        self,
        element: ElementTree.Element,
        leaves: dict[str, Leaf],
    ) -> Leaf:
        attr = self._parse_attributes(element, {"id": str})
        leaf = Leaf(attr["id"], leaf_type_from_str(element.tag))
        for edge_element in element.findall("edge"):
            e_schema: Schema = {
                "source": str,
                "destination": str,
                "bandwidth": int,
            }
            e_attr = self._parse_attributes(edge_element, e_schema)

            if not (e_attr["source"] == attr["id"]):  # type: ignore [misc]
                self._parse_error(f"Mismatched source: {e_attr['source']}")
            if e_attr["destination"] not in leaves:
                self._parse_error(f"Unknown destination: {e_attr['destination']}")

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
        self._parse_error(f"Tag unknown {node_type}")

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
            attr = self._parse_attributes(element, {"id": str})
            leaves[attr["id"]] = Leaf(attr["id"], leaf_type_from_str(node_type))
        return leaves

    def run(self, data: ElementTree.Element) -> Node:
        leaves = self.__scan_leaves(data)
        node = self.__parse_node(data, leaves)
        return node
