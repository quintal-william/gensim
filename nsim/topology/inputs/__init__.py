from typing import Any

from nsim.input import Input, InputType

from .xml import XmlTopologyInput
from .json import JsonTopologyInput
from ..models.node import Node


TopologyInput = Input[Any, Node]  # type: ignore [misc]

topology_inputs: dict[InputType, TopologyInput] = {
    InputType.JSON: JsonTopologyInput(),
    InputType.XML: XmlTopologyInput(),
}
