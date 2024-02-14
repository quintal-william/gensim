import typer

from .inputs import topology_inputs
from ..config import LoggingLevelOption, LoggingLevelDefault, get_config
from ..logger import logger
from .outputs import topology_outputs
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
from .generators import topology_generators


topology_app = typer.Typer()


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


@topology_app.command("list-generators")  # type: ignore [misc]
def topology_list_generators(
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Print a list of the available network topology generators
    """
    Commands.list_generators(topology_generators)


@topology_app.command("generate")  # type: ignore [misc]
def topology_generate(
    generator: GeneratorOption,
    output_type: OutputTypeOption = OutputTypeDefault,
    generator_config: GeneratorConfigOption = GeneratorConfigDefault,
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Generate a random network topology to some output type using a given generator
    """
    Commands.generate(
        topology_generators,
        generator,
        topology_outputs,
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
    Commands.convert(topology_inputs, input_file, topology_outputs, output_type)
