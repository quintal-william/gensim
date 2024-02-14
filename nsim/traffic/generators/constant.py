from ...generator import Generator
from ..models.traffic import Traffic
from ..models.traversal import Traversal


class ConstantTrafficGenerator(Generator[Traffic]):
    """
    Generates network traffic with a constant arrival pattern
    """

    def run(self) -> Traffic:
        node = self._get_input_node()
        duration = self._get_input_duration()
        rate = self._get_input(
            "rate",
            "the rate at which arrivals occur per second",
            "a float with value >= 0",
            float,
            lambda n: n >= 0,
        )

        traffic = Traffic(f"{node.get_id()}-traffic")
        traversal = Traversal(node)

        time = rate
        while time < duration:
            traffic.add_random_arrival(traversal, time)
            time += rate

        return traffic
