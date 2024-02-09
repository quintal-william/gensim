from enum import Enum
from typing import Annotated, Optional

import typer

from ..config import LoggingLevelDefault, LoggingLevelOption, get_config
from ..logger import logger
from ..version import VersionDefault, VersionOption


traffic_app = typer.Typer()

class TrafficOutputType(str, Enum):
    CONSOLE = "console"
    JSON = "json"
    XML = "xml"


@traffic_app.callback("traffic") # type: ignore [misc]
def traffic_main(
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Generate, read, process, and/or write network traffic
    """
    logger.debug(f"Start command traffic with config: {get_config().to_json()}")
    logger.debug("End command traffic")


@traffic_app.command("generators") # type: ignore [misc]
def traffic_list_generators(
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Print a list of the available network traffic generators
    """
    logger.debug(f"Start command traffic_generators with config: {get_config().to_json()}")
    logger.error("This function is not implemented yet")
    logger.debug("End command traffic_generate")

@traffic_app.command("generate") # type: ignore [misc]
def traffic_generate(
    generator_name: Annotated[Optional[str], typer.Option("--generator", "-g", help="The name of the generator (found using the `generators` command). If not specified, it picks a random generator", show_default=False)] = None,
    output_type: Annotated[TrafficOutputType, typer.Option("--output", "-o", help="The output type the traffic data is generated into")] = TrafficOutputType.CONSOLE,
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Generate some random network traffic to some output type using a given generator
    """
    logger.debug(f"Start command traffic_generate with config: {get_config().to_json()}")
    logger.error("This function is not implemented yet")
    logger.debug("End command traffic_generate")

@traffic_app.command("convert") # type: ignore [misc]
def traffic_convert(
    input_file: Annotated[str, typer.Argument(help="The input file with traffic data that is to be converted", show_default=False)],
    output_type: Annotated[TrafficOutputType, typer.Option("--output", "-o", help="The output type the traffic data is converted into")] = TrafficOutputType.CONSOLE,
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    Convert some network traffic from one type to another
    """
    logger.debug(f"Start command traffic_convert with config: {get_config().to_json()}")
    logger.error("This function is not implemented yet")
    logger.debug("End command traffic_convert")
