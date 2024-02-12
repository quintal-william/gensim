from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar
from collections.abc import Callable

import typer


InputType = TypeVar("InputType")
GeneratorType = TypeVar("GeneratorType")


class Generator(Generic[GeneratorType], metaclass=ABCMeta):
    @staticmethod
    def _get_input(
        input_text: str,
        validate_text: str,
        parse: Callable[[str], InputType],
        validate: Callable[[InputType], bool],
    ) -> InputType:
        while True:
            input_value: str = typer.prompt(
                f"Please enter {input_text} ({validate_text})",
            )
            try:
                parsed_input_value = parse(input_value)
                if validate(parsed_input_value):
                    return parsed_input_value
                else:
                    typer.echo(f"Input must be {validate_text}")
            except ValueError:
                typer.echo(f"Input must be {validate_text}")

    @staticmethod
    @abstractmethod
    def gen() -> GeneratorType:
        pass
