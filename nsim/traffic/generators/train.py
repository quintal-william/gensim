import random
from typing import Callable

from ...generator import Generator
from ..models.arrival import Arrival
from ..models.traffic import Traffic
from ..models.traversal import Traversal


class TrainTrafficGenerator(Generator[Traffic]):
    """
    Generates network traffic where arrivals are grouped into trains with a common source and destination
    """

    def run(self) -> Traffic:
        node = self._get_input_node()
        duration = self._get_input_duration()

        inter_train_time = self._get_input(
            "inter_train_time",
            "the average time in simulation seconds between the starts of consecutive packet trains",
            "a float with value >= 0",
            float,
            lambda n: n >= 0,
        )
        inter_car_time = self._get_input(
            "inter_car_time",
            "the average time in simulation seconds between packets within a train",
            "a float with value >= 0",
            float,
            lambda n: n >= 0,
        )
        max_train_length = self._get_input(
            "max_train_length",
            "the maximum number of packets in a train",
            "an integer with value >= 0",
            int,
            lambda n: n >= 0,
        )

        traffic = Traffic(f"{node.get_id()}-traffic")
        traversal = Traversal(node)

        r: Callable[[float], float] = lambda x: random.expovariate(1.0 / x)

        time = r(inter_train_time)
        while time < duration:
            route = traversal.get_random_route()
            source = route.get_source().get_id()
            destination = route.get_destination().get_id()
            for i in range(random.randint(1, max_train_length)):
                if i != 0:
                    time += r(inter_car_time)
                if time > duration:
                    break
                traffic.add_arrival(Arrival(time, source, destination))
            time += r(inter_train_time)

        return traffic
