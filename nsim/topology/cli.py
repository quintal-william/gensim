from enum import Enum
from random import choice
from typing import Optional, Annotated

import typer
from rich import print

from nsim.input import Input
from nsim.output import Output
from nsim.generator import Generator

from ..util import fatal
from ..config import LoggingLevelOption, LoggingLevelDefault, get_config
from ..logger import logger
from ..version import VersionOption, VersionDefault
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


def select_generator(generator_name: Optional[str]) -> Generator[Node]:
    # Pick random generator if none specified
    if generator_name == None:
        generator_name = choice(list(generators.keys()))
        logger.debug(f"No generator specified, picked '{generator_name}' at random")

    # Select generator
    try:
        if generator_name:
            generator = generators[generator_name]
        else:
            fatal("No generator name given")
    except KeyError:
        fatal(
            f"Generator {generator_name} was not recognized. Please run `nsim topology generators` to see a list of valid generators",
        )

    logger.debug(f"Selected generator {generator_name}")
    return generator


class TopologyOutputType(str, Enum):
    CONSOLE = "console"
    JSON = "json"
    XML = "xml"
    OMNEST = "omnest"


outputs: dict[TopologyOutputType, Output[Node]] = {
    TopologyOutputType.CONSOLE: ConsoleTopologyOutput(),
    TopologyOutputType.JSON: JsonTopologyOutput(),
    TopologyOutputType.XML: XmlTopologyOutput(),
    # TopologyOutputType.OMNEST: OmnestTopologyOutput(),
}


def select_output(output_type: TopologyOutputType) -> Output[Node]:
    try:
        output = outputs[output_type]
    except KeyError:
        fatal(
            f"Output type {output_type} was not recognized. Please use one of the allowed values",
        )

    logger.debug(f"Selected output type {output_type}")
    return output


class TopologyInputType(str, Enum):
    JSON = "json"
    XML = "xml"


inputs: dict[TopologyInputType, Input[Node]] = {
    TopologyInputType.JSON: JsonTopologyInput(),
    TopologyInputType.XML: XmlTopologyInput(),
}


def select_input(input_type: TopologyInputType) -> Input[Node]:
    try:
        i = inputs[input_type]
    except KeyError:
        fatal(
            f"Input type {input_type} was not recognized. Please use one of the allowed values",
        )

    logger.debug(f"Selected input type {i}")
    return i


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
    logger.debug(
        f"Start command topology_generators with config: {get_config().to_json()}",
    )

    for generator_name, generator in generators.items():
        doc = generator.__doc__
        if doc:
            print(f"[bold bright_yellow]{generator_name}[/]: {doc.strip()}")
        else:
            print(f"[bold bright_yellow]{generator_name}[/]")

    logger.debug("End command topology_generators")


@topology_app.command("generate")  # type: ignore [misc]
def topology_generate(
    generator_name: Annotated[
        Optional[str],
        typer.Option(
            "--generator",
            "-g",
            help="The name of the generator (found using the `generators` command). If not specified, it picks a random generator",
            show_default=False,
        ),
    ] = None,
    output_type: Annotated[
        TopologyOutputType,
        typer.Option(
            "--output",
            "-o",
            help="The output type the topology data is generated into",
        ),
    ] = TopologyOutputType.CONSOLE,
    generator_config: Annotated[
        Optional[str],
        typer.Option(
            "--generator-config",
            "-c",
            help="A JSON object with configuration options for the generator",
            show_default=False,
        ),
    ] = None,
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Generate a random network topology to some output type using a given generator
    """
    logger.debug(
        f"Start command topology_generate with config: {get_config().to_json()}",
    )

    generator = select_generator(generator_name)
    output = select_output(output_type)

    logger.debug("Generating topology")
    topology = generator.run_super(generator_config)

    logger.debug("Printing generated topology")
    output.run_super(topology)

    logger.debug("End command topology_generate")


@topology_app.command("convert")  # type: ignore [misc]
def topology_convert(
    input_file: Annotated[
        str,
        typer.Argument(
            help="The input file with topology data that is to be converted",
            show_default=False,
        ),
    ],
    output_type: Annotated[
        TopologyOutputType,
        typer.Option(
            "--output",
            "-o",
            help="The output type the topology data is converted into",
        ),
    ] = TopologyOutputType.CONSOLE,
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Convert a network topology from one type to another
    """
    logger.debug(
        f"Start command topology_convert with config: {get_config().to_json()}",
    )

    logger.debug(f"Reading file: {input_file}")
    split_input = input_file.split(".")

    if len(split_input) <= 1:
        fatal("File extension could not be read from input file.")

    ext = split_input[-1]

    match ext:
        case "xml":
            logger.debug("Detected input file type XML")
            i = select_input(TopologyInputType.XML)
        case "json":
            logger.debug("Detected input file type JSON")
            i = select_input(TopologyInputType.JSON)
        case _:
            fatal(
                "Unknown input file type. Please supply an input file with a *.json, or *.xml file extension.",
            )

    output = select_output(output_type)

    content = i.run_super(input_file)

    logger.debug("Printing converted topology")
    output.run_super(content)

    logger.debug("End command topology_convert")
