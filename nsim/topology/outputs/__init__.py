from nsim.output import Output, OutputType

from .xml import XmlTopologyOutput
from .json import JsonTopologyOutput
from .console import ConsoleTopologyOutput
from ..models.node import Node


topology_outputs: dict[OutputType, Output[Node]] = {
    OutputType.CONSOLE: ConsoleTopologyOutput(),
    OutputType.JSON: JsonTopologyOutput(),
    OutputType.XML: XmlTopologyOutput(),
    # OutputType.OMNEST: OmnestTopologyOutput(),
}
