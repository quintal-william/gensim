import random

from ...generator import Generator
from ..models.traffic import Traffic
from ..models.traversal import Traversal


class PoissonTrafficGenerator(Generator[Traffic]):
    """
    Generates network traffic with an exponential arrival pattern
    """

    def run(self) -> Traffic:
        node = self._get_input_node()
        duration = self._get_input_duration()
        l = self._get_input(
            "lambda",
            "the mean rate at which arrivals occur per second",
            "a float with value >= 0",
            float,
            lambda n: n >= 0,
        )

        traffic = Traffic(f"{node.get_id()}-traffic")
        traversal = Traversal(node)

        time = random.expovariate(l)
        while time < duration:
            traffic.add_random_arrival(traversal, time)
            time += random.expovariate(l)

        # Test poisson property
        # arrivals_per_time_unit: dict[int, int] = {}
        # for arrival in traffic.get_arrivals():
        #     bucket = math.floor(arrival.get_time())
        #     arrivals_per_time_unit.setdefault(bucket, 0)
        #     arrivals_per_time_unit[bucket] += 1

        # mean = sum(arrivals_per_time_unit.values()) / len(arrivals_per_time_unit)
        # variance = sum((x - mean) ** 2 for x in arrivals_per_time_unit.values()) / len(arrivals_per_time_unit)
        # r: Callable[[float], str] = "{:.4f}".format

        # print(f"Lambda: {l}")
        # print(f"Sample mean: {r(mean)}     (diff: {r(abs(mean-l))})")
        # print(f"Sample variance: {r(variance)} (diff: {r(abs(variance-l))})")
        # print()

        return traffic
