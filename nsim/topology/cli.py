from typing import Any

import typer

from nsim.input import Input, InputType
from nsim.output import Output, OutputType
from nsim.generator import Generator

from ..config import LoggingLevelOption, LoggingLevelDefault, get_config
from ..logger import logger
from ..version import VersionOption, VersionDefault
from ..commands import (
    Commands,
    GeneratorOption,
    OutputTypeOption,
    InputFileArgument,
    OutputTypeDefault,
    GeneratorConfigOption,
    GeneratorConfigDefault,
)
from .inputs.xml import XmlTopologyInput
from .inputs.json import JsonTopologyInput
from .models.node import Node
from .outputs.xml import XmlTopologyOutput
from .outputs.json import JsonTopologyOutput
from .generators.mesh import MeshTopologyGenerator
from .generators.star import StarTopologyGenerator
from .outputs.console import ConsoleTopologyOutput


topology_app = typer.Typer()

generators: dict[str, Generator[Node]] = {
    "mesh": MeshTopologyGenerator(),
    "star": StarTopologyGenerator(),
}

outputs: dict[OutputType, Output[Node]] = {
    OutputType.CONSOLE: ConsoleTopologyOutput(),
    OutputType.JSON: JsonTopologyOutput(),
    OutputType.XML: XmlTopologyOutput(),
    # TopologyOutputType.OMNEST: OmnestTopologyOutput(),
}

TopologyInput = Input[Any, Node]  # type: ignore [misc]

inputs: dict[InputType, TopologyInput] = {
    InputType.JSON: JsonTopologyInput(),
    InputType.XML: XmlTopologyInput(),
}


@topology_app.callback("topology")  # type: ignore [misc]
def topology_main(
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Generate, read, process, and/or write network topologies
    """
    logger.debug(f"Start command topology with config: {get_config().to_json()}")
    logger.debug("End command topology")


@topology_app.command("generators")  # type: ignore [misc]
def topology_generators(
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Print a list of the available network topology generators
    """
    Commands.generators(generators)


@topology_app.command("generate")  # type: ignore [misc]
def topology_generate(
    generator_name: GeneratorOption,
    output_type: OutputTypeOption = OutputTypeDefault,
    generator_config: GeneratorConfigOption = GeneratorConfigDefault,
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Generate a random network topology to some output type using a given generator
    """
    Commands.generate(
        generators,
        generator_name,
        outputs,
        output_type,
        generator_config,
    )


@topology_app.command("convert")  # type: ignore [misc]
def topology_convert(
    input_file: InputFileArgument,
    output_type: OutputTypeOption = OutputTypeDefault,
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Convert a network topology from one type to another
    """
    Commands.convert(inputs, input_file, outputs, output_type)
