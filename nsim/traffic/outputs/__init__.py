from nsim.output import Output, OutputType

from .console import ConsoleTrafficOutput
from .json import JsonTrafficOutput
from .xml import XmlTrafficOutput
from ..models.traffic import Traffic


traffic_outputs: dict[OutputType, Output[Traffic]] = {
    OutputType.CONSOLE: ConsoleTrafficOutput(),
    OutputType.JSON: JsonTrafficOutput(),
    OutputType.XML: XmlTrafficOutput(),
    # OutputType.OMNEST: OmnestTrafficOutput(),
}
