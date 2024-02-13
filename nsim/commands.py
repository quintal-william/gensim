from typing import Any, Generic, TypeVar, Optional, Annotated

import typer
from rich import print

from .util import fatal
from .input import Input, InputType
from .config import get_config
from .logger import logger
from .output import Output, OutputType
from .generator import Generator


GeneratorOption = Annotated[
    str,
    typer.Option(
        "--generator",
        "-g",
        help="The name of the generator (found using the `generators` command)",
    ),
]

OutputTypeOption = Annotated[
    OutputType,
    typer.Option(
        "--output",
        "-o",
        help="The output type the data is converted into",
    ),
]

OutputTypeDefault = OutputType.CONSOLE

GeneratorConfigOption = Annotated[
    Optional[str],
    typer.Option(
        "--generator-config",
        "-c",
        help="A JSON object with configuration options for the generator",
        show_default=False,
    ),
]

GeneratorConfigDefault = None

InputFileArgument = Annotated[
    str,
    typer.Argument(
        help="The input file with data that is to be converted",
        show_default=False,
    ),
]

T = TypeVar("T")
TKey = TypeVar("TKey")
TValue = TypeVar("TValue")
AnyInput = Input[Any, T]  # type: ignore [misc]


class Commands(Generic[T]):
    @staticmethod
    def __select(name: str, items: dict[TKey, TValue], key: TKey) -> TValue:
        try:
            item = items[key]
        except KeyError:
            fatal(
                f"{name} '{key}' was not recognized. Please use one of the allowed values: {items.keys()}",
            )

        logger.debug(f"Selected {name} {item}")
        return item

    @staticmethod
    def generators(generators: dict[str, Generator[T]]) -> None:
        logger.debug(f"Start command generators with config: {get_config().to_json()}")

        for generator_name, generator in generators.items():
            doc = generator.__doc__
            if doc:
                print(f"[bold bright_yellow]{generator_name}[/]: {doc.strip()}")
            else:
                print(f"[bold bright_yellow]{generator_name}[/]")

        logger.debug("End command generators")

    @staticmethod
    def generate(
        generators: dict[str, Generator[T]],
        generator_name: GeneratorOption,
        outputs: dict[OutputType, Output[T]],
        output_type: OutputTypeOption,
        generator_config: GeneratorConfigOption,
    ) -> None:
        logger.debug(f"Start command generate with config: {get_config().to_json()}")

        generator = Commands.__select("generator", generators, generator_name)
        output = Commands.__select("output", outputs, output_type)

        logger.debug("Start generator")
        generated = generator.run_super(generator_config)
        logger.debug("End generator")

        logger.debug("Start output")
        output.run_super(generated)
        logger.debug("End output")

        logger.debug("End command generate")

    @staticmethod
    def convert(
        inputs: dict[InputType, AnyInput[T]],
        input_file: InputFileArgument,
        outputs: dict[OutputType, Output[T]],
        output_type: OutputTypeOption,
    ) -> None:
        logger.debug(f"Start command convert with config: {get_config().to_json()}")

        logger.debug(f"Reading file: {input_file}")
        split_input = input_file.split(".")

        if len(split_input) <= 1:
            fatal("File extension could not be read from input file.")

        ext = split_input[-1]

        match ext:
            case "xml":
                logger.debug("Detected input file type XML")
                i = Commands.__select("input", inputs, InputType.XML)
            case "json":
                logger.debug("Detected input file type JSON")
                i = Commands.__select("input", inputs, InputType.JSON)
            case _:
                fatal(
                    "Unknown input file type. Please supply an input file with a *.json, or *.xml file extension.",
                )

        output = Commands.__select("output", outputs, output_type)

        logger.debug("Start input")
        content = i.run_super(input_file)
        logger.debug("End input")

        logger.debug("Start output")
        output.run_super(content)
        logger.debug("End output")

        logger.debug("End command convert")
