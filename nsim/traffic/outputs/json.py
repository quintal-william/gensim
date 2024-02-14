import json

from nsim.output import JsonOutput

from ...util import Json
from ..models.arrival import Arrival
from ..models.traffic import Traffic


class JsonTrafficOutput(JsonOutput[Traffic]):
    def __make_arrival_data(self, arrival: Arrival) -> Json:
        data = self._make_item(arrival.__class__.__name__, arrival.get_id())
        data["time"] = arrival.get_time()
        data["source"] = arrival.get_source()
        data["destination"] = arrival.get_destination()
        data["size"] = arrival.get_size()
        return data

    def __make_traffic_data(self, traffic: Traffic) -> Json:
        data = self._make_item(traffic.__class__.__name__, traffic.get_id())
        arrivals_data: list[Json] = []
        data["arrivals"] = arrivals_data
        for arrival in traffic.get_arrivals():
            data["arrivals"].append(self.__make_arrival_data(arrival))
        return data

    def run(self, traffic: Traffic) -> None:
        data = self.__make_traffic_data(traffic)
        print(json.dumps(data, indent=2))
