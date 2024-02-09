import typer

from .config import LoggingLevelDefault, LoggingLevelOption, get_config
from .logger import logger
from .topology.cli import topology_app
from .traffic.cli import traffic_app
from .version import VersionDefault, VersionOption


app = typer.Typer()
app.add_typer(topology_app)
app.add_typer(traffic_app)

@app.callback() # type: ignore [misc]
def main(
    version: VersionOption = VersionDefault,
    logging_level: LoggingLevelOption = LoggingLevelDefault,
) -> None:
    """
    A CLI tool to generate and transform network topologies and traffic data for the DSE2.0 research project
    """
    logger.debug(f"Set config to: {get_config().to_json()}")
