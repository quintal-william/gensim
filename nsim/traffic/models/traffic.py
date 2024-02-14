from ...model import Model
from .arrival import Arrival
from .traversal import Traversal


class Traffic(Model):
    """
    Data structure that holds arrivals
    """

    __arrivals: list[Arrival] = []

    def add_arrival(self, arrival: Arrival) -> None:
        self.__arrivals.append(arrival)

    def add_random_arrival(self, traversal: Traversal, time: float) -> None:
        route = traversal.get_random_route()
        source = route.get_source().get_id()
        destination = route.get_destination().get_id()
        self.add_arrival(Arrival(time, source, destination))

    def get_arrivals(self) -> list[Arrival]:
        return self.__arrivals.copy()
