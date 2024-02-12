from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

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
