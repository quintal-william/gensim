from xml.etree import ElementTree

from nsim.output import XmlOutput

from ..models.arrival import Arrival
from ..models.traffic import Traffic


class XmlTrafficOutput(XmlOutput[Traffic]):
    def __make_arrival_element(self, arrival: Arrival) -> ElementTree.Element:
        attributes: dict[str, str] = {
            "time": str(arrival.get_time()),
            "source": arrival.get_source(),
            "destination": arrival.get_destination(),
            "size": str(arrival.get_size()),
        }
        arrival_type = arrival.__class__.__name__.lower()
        return self._make_element(arrival_type, arrival.get_id(), attributes)

    def __make_traffic_element(self, traffic: Traffic) -> ElementTree.Element:
        element = self._make_element(
            traffic.__class__.__name__.lower(),
            traffic.get_id(),
        )
        for arrival in traffic.get_arrivals():
            element.append(self.__make_arrival_element(arrival))
        return element

    def run(self, traffic: Traffic) -> None:
        element = self.__make_traffic_element(traffic)
        ElementTree.indent(element)
        print(ElementTree.tostring(element, encoding="unicode"))
