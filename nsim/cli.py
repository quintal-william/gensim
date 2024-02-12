import typer

from .config import LoggingLevelOption, LoggingLevelDefault, get_config
from .logger import logger
from .version import VersionOption, VersionDefault
from .traffic.cli import traffic_app
from .topology.cli import topology_app


app = typer.Typer()
app.add_typer(topology_app)
app.add_typer(traffic_app)


@app.callback()  # type: ignore [misc]
def main(
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    A CLI tool to generate and transform network topologies and traffic data for the DSE2.0 research project
    """
    logger.debug(f"Set config to: {get_config().to_json()}")
