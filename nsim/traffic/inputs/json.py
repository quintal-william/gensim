from typing import TypedDict, TypeGuard

from ...util import Json
from ...input import JsonInput
from ..models.arrival import Arrival
from ..models.traffic import Traffic


class ArrivalSchema(TypedDict):
    type: str
    id: str
    time: float
    source: str
    destination: str
    size: int


class TrafficSchema(TypedDict):
    type: str
    id: str
    arrivals: list[Json]


class JsonTrafficInput(JsonInput[Traffic]):
    def __validate_arrival(self, data: Json) -> TypeGuard[ArrivalSchema]:
        schema: Json = ArrivalSchema.__annotations__
        return self._validate_schema(data, schema)

    def __validate_traffic(self, data: Json) -> TypeGuard[TrafficSchema]:
        schema: Json = TrafficSchema.__annotations__
        return self._validate_schema(data, schema)

    def __parse_arrival(self, data: Json) -> Arrival:
        if self.__validate_arrival(data) and data["type"] == "Arrival":
            return Arrival(
                data["time"],
                data["source"],
                data["destination"],
                data["size"],
            )
        self._parse_error(f'Unrecognised arrival type: {data["type"]}')

    def __parse_traffic(self, data: Json) -> Traffic:
        if self.__validate_traffic(data) and data["type"] == "Traffic":
            traffic = Traffic(data["id"])
            for arrival in data["arrivals"]:
                traffic.add_arrival(self.__parse_arrival(arrival))
            return traffic

        self._parse_error(f'Unrecognised traffic type: {data["type"]}')

    def run(self, data: Json) -> Traffic:
        return self.__parse_traffic(data)
