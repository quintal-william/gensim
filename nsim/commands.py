from typing import Any, Generic, TypeVar, Optional, Annotated

import typer
from rich import print

from .util import select, get_file_path_extension
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
        help="The name of the generator (found using the `list-generators` command)",
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
AnyInput = Input[Any, T]  # type: ignore [misc]


class Commands(Generic[T]):
    @staticmethod
    def list_generators(generators: dict[str, Generator[T]]) -> None:
        logger.debug(
            f"Start command list-generators with config: {get_config().to_json()}",
        )

        for generator_name, generator in generators.items():
            doc = generator.__doc__
            if doc:
                print(f"[bold bright_yellow]{generator_name}[/]: {doc.strip()}")
            else:
                print(f"[bold bright_yellow]{generator_name}[/]")

        logger.debug("End command list-generators")

    @staticmethod
    def generate(
        generators: dict[str, Generator[T]],
        generator_name: GeneratorOption,
        outputs: dict[OutputType, Output[T]],
        output_type: OutputTypeOption,
        generator_config: GeneratorConfigOption,
    ) -> None:
        logger.debug(f"Start command generate with config: {get_config().to_json()}")

        generator = select("generator", generators, generator_name)
        output = select("output", outputs, output_type)

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

        i = select("input", inputs, InputType(get_file_path_extension(input_file)))
        output = select("output", outputs, output_type)

        logger.debug("Start input")
        content = i.run_super(input_file)
        logger.debug("End input")

        logger.debug("Start output")
        output.run_super(content)
        logger.debug("End output")

        logger.debug("End command convert")
