from typing import Any, NoReturn

import typer

from .logger import logger


"""
A number between 0 and 1 which represents the probability of two nodes being connected
"""
Connectivity = float

"""
Helper type for working with json data
"""
Json = dict[str, Any]  # type: ignore [misc]


def fatal(message: str) -> NoReturn:
    """
    Log a fatal error to the console and exit, never return
    """
    logger.error(f"Error loading or parsing JSON data: {message}")
    raise typer.Exit()
