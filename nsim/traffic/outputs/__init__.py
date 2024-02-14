from nsim.output import Output, OutputType

from .xml import XmlTrafficOutput
from .json import JsonTrafficOutput
from .console import ConsoleTrafficOutput
from ..models.traffic import Traffic


traffic_outputs: dict[OutputType, Output[Traffic]] = {
    OutputType.CONSOLE: ConsoleTrafficOutput(),
    OutputType.JSON: JsonTrafficOutput(),
    OutputType.XML: XmlTrafficOutput(),
    # OutputType.OMNEST: OmnestTrafficOutput(),
}
