from ...output import ConsoleOutput
from ..models.arrival import Arrival
from ..models.traffic import Traffic


class ConsoleTrafficOutput(ConsoleOutput[Traffic]):
    def __print_arrival(self, arrival: Arrival) -> None:
        a_type = arrival.__class__.__name__
        a_id = arrival.get_id()
        self._print(a_type, a_id, depth=1)

    def __print_traffic(self, traffic: Traffic) -> None:
        t_type = traffic.__class__.__name__
        t_id = traffic.get_id()
        t_arrivals = traffic.get_arrivals()

        if len(t_arrivals) == 0:
            self._print(t_type, t_id, message="has no traffic")
        else:
            self._print(t_type, t_id, message="has arrivals:")
            for arrival in t_arrivals:
                self.__print_arrival(arrival)

    def run(self, traffic: Traffic) -> None:
        self.__print_traffic(traffic)
