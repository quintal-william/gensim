from __future__ import annotations

from enum import Enum

from .edge import Edge
from .node import Node


class LeafType(Enum):
  HOST = "HOST"
  SWITCH = "SWITCH"


class Leaf(Node):
  '''
  Represents the smallest possible unit in a network (e.g. Host, Switch)
  '''

  __edges: list[Edge]
  __type: LeafType

  def __init__(self, id: str, type: LeafType) -> None:
    super().__init__(id)
    self.__type = type
    self.__edges = []

  def flatten(self) -> list[Leaf]:
    return [self]

  def add_edge(self, destination: Leaf, bandwidth: int) -> None:
    edge = Edge(
      source = self,
      destination = destination,
      bandwidth = bandwidth,
    )
    self.__edges.append(edge)

  def get_edges(self) -> list[Edge]:
    return self.__edges.copy()

  def get_type(self) -> LeafType:
    return self.__type
