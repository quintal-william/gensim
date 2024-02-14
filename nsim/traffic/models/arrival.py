import random

from ...model import Model


class Arrival(Model):
    """
    Represents a message entering the network
    """

    __time: float  # Simulation time
    __source: str  # Node ID
    __destination: str  # Node ID
    __size: int  # In bytes

    def __init__(
        self,
        time: float,
        source: str,
        destination: str,
        size_optional: int | None = None,
    ) -> None:
        size: int = size_optional or random.randint(512, 1500)  # Typical TCP/IP traffic

        super().__init__(f"{time}_{source}_{destination}_{size}")
        self.__time = time
        self.__source = source
        self.__destination = destination
        self.__size = size

    def get_time(self) -> float:
        return self.__time

    def get_source(self) -> str:
        return self.__source

    def get_destination(self) -> str:
        return self.__destination

    def get_size(self) -> int:
        return self.__size
