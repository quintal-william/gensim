import xml.etree.ElementTree as ElementTree

from nsim.input import Schema, XmlInput

from ..models.arrival import Arrival
from ..models.traffic import Traffic


class XmlTrafficInput(XmlInput[Traffic]):
    def __parse_arrival(self, element: ElementTree.Element) -> Arrival:
        schema: Schema = {
            "id": str,
            "time": float,
            "source": str,
            "destination": str,
            "size": int,
        }
        attr = self._parse_attributes(element, schema)
        return Arrival(attr["time"], attr["source"], attr["destination"], attr["size"])

    def __parse_traffic(self, element: ElementTree.Element) -> Traffic:
        attr = self._parse_attributes(element, {"id": str})
        traffic = Traffic(attr["id"])
        for arrival in element.findall("arrival"):
            traffic.add_arrival(self.__parse_arrival(arrival))
        return traffic

    def run(self, data: ElementTree.Element) -> Traffic:
        return self.__parse_traffic(data)
