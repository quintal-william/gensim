from typing import Any

from nsim.input import Input, InputType

from ..models.traffic import Traffic


TrafficInput = Input[Any, Traffic]  # type: ignore [misc]

traffic_inputs: dict[InputType, TrafficInput] = {
    # InputType.JSON: JsonTrafficInput(),
    # InputType.XML: XmlTrafficInput(),
}