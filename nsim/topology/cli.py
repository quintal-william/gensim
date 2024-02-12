from enum import Enum
from random import choice
from typing import Optional, Annotated

import typer
from rich import print
from rich.progress import Progress, TextColumn, SpinnerColumn

from nsim.input import Input
from nsim.output import Output
from nsim.generator import Generator

from ..config import LoggingLevelOption, LoggingLevelDefault, get_config
from ..logger import logger
from ..version import VersionOption, VersionDefault
from .inputs.xml import XmlTopologyInput
from .inputs.json import JsonTopologyInput
from .models.node import Node
from .outputs.xml import XmlTopologyOutput
from .outputs.json import JsonTopologyOutput
from .outputs.omnest import OmnestTopologyOutput
from .generators.mesh import MeshTopologyGenerator
from .outputs.console import ConsoleTopologyOutput


topology_app = typer.Typer()

generators: dict[str, type[Generator[Node]]] = {
    "mesh": MeshTopologyGenerator,
    # "star": FullStarTopologyGenerator,
}


def select_generator(generator_name: Optional[str]) -> type[Generator[Node]]:
    # Pick random generator if none specified
    if generator_name == None:
        generator_name = choice(list(generators.keys()))
        logger.debug(f"No generator specified, picked '{generator_name}' at random")

    # Select generator
    try:
        if generator_name:
            generator = generators[generator_name]
        else:
            logger.error("No generator name given")
            raise typer.Exit()
    except KeyError:
        logger.error(
            f"Generator {generator_name} was not recognized. Please run `nsim topology generators` to see a list of valid generators",
        )
        raise typer.Exit()

    logger.debug(f"Selected generator {generator_name}")
    return generator


class TopologyOutputType(str, Enum):
    CONSOLE = "console"
    JSON = "json"
    XML = "xml"
    OMNEST = "omnest"  # TODO ask for abstraction level (INET, LATENCY RATE, etc), and standalone or embedded


outputs: dict[TopologyOutputType, type[Output[Node]]] = {
    TopologyOutputType.CONSOLE: ConsoleTopologyOutput,
    TopologyOutputType.JSON: JsonTopologyOutput,
    TopologyOutputType.XML: XmlTopologyOutput,
    TopologyOutputType.OMNEST: OmnestTopologyOutput,
}


def select_output(output_type: TopologyOutputType) -> type[Output[Node]]:
    try:
        output = outputs[output_type]
    except KeyError:
        logger.error(
            f"Output type {output_type} was not recognized. Please use one of the allowed values",
        )
        raise typer.Exit()

    logger.debug(f"Selected output type {output_type}")
    return output


class TopologyInputType(str, Enum):
    JSON = "json"
    XML = "xml"


inputs: dict[TopologyInputType, type[Input]] = {
    TopologyInputType.JSON: JsonTopologyInput,
    TopologyInputType.XML: XmlTopologyInput,
}


def select_input(input_type: TopologyInputType) -> type[Input]:
    try:
        i = inputs[input_type]
    except KeyError:
        logger.error(
            f"Input type {input_type} was not recognized. Please use one of the allowed values",
        )
        raise typer.Exit()

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

    # with Progress(
    #     SpinnerColumn(),
    #     TextColumn("[progress.description]{task.description}"),
    #     transient=True,
    # ) as progress:
    #     progress.add_task(description="Generating...", total=None)

    logger.debug("Generating topology")
    topology = generator.gen()

    logger.debug("Printing generated topology")
    output.dump(topology)  # type: ignore [arg-type]

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

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Reading...", total=None)

        logger.debug(f"Reading file: {input_file}")
        split_input = input_file.split(".")

        if len(split_input) <= 1:
            logger.error("File extension could not be read from input file.")
            raise typer.Exit()

        ext = split_input[-1]

        match ext:
            case "xml":
                logger.info("Detected input file type XML")
                i = select_input(TopologyInputType.XML)
            case "json":
                logger.info("Detected input file type JSON")
                i = select_input(TopologyInputType.JSON)
            case _:
                logger.error(
                    "Unknown input file type. Please supply an input file with a *.json, or *.xml file extension.",
                )
                raise typer.Exit()

        content = i.load(input_file)

        logger.debug("Writing")
        o = select_output(output_type)
        o.dump(content)

    logger.debug("End command topology_convert")
