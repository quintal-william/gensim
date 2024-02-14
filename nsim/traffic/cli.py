import typer

from .inputs import traffic_inputs
from ..config import LoggingLevelOption, LoggingLevelDefault, get_config
from ..logger import logger
from .outputs import traffic_outputs
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
from .generators import traffic_generators


traffic_app = typer.Typer()


@traffic_app.callback("traffic")  # type: ignore [misc]
def traffic_main(
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Generate, read, process, and/or write network traffic
    """
    logger.debug(f"Start command traffic with config: {get_config().to_json()}")
    logger.debug("End command traffic")


@traffic_app.command("list-generators")  # type: ignore [misc]
def traffic_list_generators(
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Print a list of the available network traffic generators
    """
    Commands.list_generators(traffic_generators)


@traffic_app.command("generate")  # type: ignore [misc]
def traffic_generate(
    generator: GeneratorOption,
    output_type: OutputTypeOption = OutputTypeDefault,
    generator_config: GeneratorConfigOption = GeneratorConfigDefault,
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Generate random network traffic to some output type using a given generator
    """
    Commands.generate(
        traffic_generators,
        generator,
        traffic_outputs,
        output_type,
        generator_config,
    )


@traffic_app.command("convert")  # type: ignore [misc]
def traffic_convert(
    input_file: InputFileArgument,
    output_type: OutputTypeOption = OutputTypeDefault,
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Convert network traffic data from one type to another
    """
    Commands.convert(traffic_inputs, input_file, traffic_outputs, output_type)
