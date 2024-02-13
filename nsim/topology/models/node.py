from __future__ import annotations

import random
from abc import abstractmethod
from typing import TYPE_CHECKING

from ...util import Connectivity
from ...model import Model


if TYPE_CHECKING:
    from .leaf import Leaf


class Node(Model):
    """
    Represents anything that can be (sub-)connected to anything
    """

    @abstractmethod
    def flatten(self) -> list[Leaf]:
        pass

    def connect(
        self,
        node_b: Node,
        connectivity: Connectivity,
        bandwidth: int | None = None,
    ) -> None:
        if bandwidth == None:
            bandwidths = [
                10000000,  # 10BASE-T, 10 Mbps, rarely used in modern settings
                100000000,  # 100BASE-TX, 100 Mbps, in use for some home networks
                1000000000,  # 1000BASE-T, 1 Gbps, common in modern home networks
                10000000000,  # 10GBASE-T, 10 Gbps, used in enterprise networks and data centers
                25000000000,  # 25GBASE-T, 25 Gbps, increasingly adopted in data centers
                40000000000,  # 40GBASE-T, 40 Gbps, used in high-speed backbones of data center networks
                100000000000,  # 100GBASE-T, 100 Gbps, used in large data centers and internet backbones
            ]
            bandwidth = random.choice(bandwidths)

        for a in self.flatten():
            for b in node_b.flatten():
                if connectivity > random.random():
                    bandwidth = random.choice(bandwidths)
                    a.add_edge(b, bandwidth)
                    b.add_edge(a, bandwidth)
