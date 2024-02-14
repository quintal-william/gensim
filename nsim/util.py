from typing import Any, TypeVar, NoReturn

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
    logger.error(message)
    raise typer.Exit()


TKey = TypeVar("TKey")
TValue = TypeVar("TValue")


def select(name: str, items: dict[TKey, TValue], key: TKey) -> TValue:
    """
    Grab a value from a dictionary with custom error handling and logging
    """
    try:
        item = items[key]
    except KeyError:
        fatal(
            f"{name} '{key}' was not recognized. Please use one of the allowed values: {list(items.keys())}",
        )

    logger.debug(f"Selected {name} {item}")
    return item


def get_file_path_extension(file_path: str) -> str:
    """
    Get the file extension given a path
    """
    split_file_path = file_path.split(".")

    if len(split_file_path) <= 1:
        fatal(f"File extension could not be read from file path: {file_path}")

    return split_file_path[-1]
