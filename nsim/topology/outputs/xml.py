from xml.etree import ElementTree

from nsim.output import Output

from ..models.edge import Edge
from ..models.leaf import Leaf
from ..models.node import Node
from ..models.topology import Topology


class XmlTopologyOutput(Output[Node]):
    def __make_element(
        self,
        item_type: str,
        item_id: str,
        attributes: dict[str, str] | None = None,
    ) -> ElementTree.Element:
        attributes = attributes or {}
        attributes["id"] = item_id
        element = ElementTree.Element(item_type, attrib=attributes)
        return element

    def __make_edge_element(self, edge: Edge) -> ElementTree.Element:
        attributes: dict[str, str] = {
            "source": edge.get_source().get_id(),
            "destination": edge.get_destination().get_id(),
            "bandwidth": str(edge.get_bandwidth()),
        }
        edge_type = edge.__class__.__name__.lower()
        return self.__make_element(edge_type, edge.get_id(), attributes)

    def __make_leaf_element(self, leaf: Leaf) -> ElementTree.Element:
        element = self.__make_element(leaf.get_type().value.lower(), leaf.get_id())
        for edge in leaf.get_edges():
            element.append(self.__make_edge_element(edge))
        return element

    def __make_topology_element(self, topology: Topology) -> ElementTree.Element:
        topology_type = topology.__class__.__name__.lower()
        element = self.__make_element(topology_type, topology.get_id())
        for node in topology.get_nodes():
            element.append(self.__make_node_element(node))
        return element

    def __make_node_element(self, node: Node) -> ElementTree.Element:
        if isinstance(node, Leaf):
            return self.__make_leaf_element(node)
        if isinstance(node, Topology):
            return self.__make_topology_element(node)
        return self.__make_element(node.__class__.__name__.lower(), node.get_id())

    def run(self, node: Node) -> None:
        element = self.__make_node_element(node)
        ElementTree.indent(element)
        print(ElementTree.tostring(element, encoding="unicode"))
