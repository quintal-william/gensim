from typing import Annotated

import typer

from nsim import __app_name__, __version__


def __version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

VersionOption = Annotated[
    bool, typer.Option(
        "--version",
        "-v",
        help="Print the version of the CLI application",
        callback=__version_callback,
        is_eager=True,
    ),
]

VersionDefault = False
