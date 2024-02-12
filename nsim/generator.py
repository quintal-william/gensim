import json
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar
from collections.abc import Callable

import typer

from .types import Json, Connectivity
from .logger import logger


InputType = TypeVar("InputType")
GeneratorType = TypeVar("GeneratorType")


class Generator(Generic[GeneratorType], metaclass=ABCMeta):
    def _get_input(
        self,
        generator_options: str | None,
        variable_name: str,
        input_text: str,
        validate_text: str,
        parse: Callable[[str], InputType],
        validate: Callable[[InputType], bool],
    ) -> InputType:
        logger.debug(f"Collecting input for `{variable_name}`")

        if generator_options is not None:
            skip = False
            if not skip:
                try:
                    opts: Json = json.loads(generator_options)
                    logger.debug("Successfully loaded generator_options")
                except:
                    skip = True
                    logger.warn(
                        "generator_options was provided, but is not valid JSON. Skipping.",
                    )
            if not skip:
                try:
                    opt_value = opts[variable_name]
                    if not isinstance(opt_value, str):
                        raise ValueError()
                    logger.debug(f"Collected input from generator_options: {opt_value}")
                except:
                    skip = True
                    logger.warn(
                        f"generator_options was provided, but `{variable_name}` is not a valid key. Skipping.",
                    )
            if not skip:
                try:
                    parsed_opt_value = parse(opt_value)
                    logger.debug(f"Parsed input from generator_options: {parsed_opt_value}")
                except:
                    skip = True
                    logger.warn(
                        f"Value was provided in generator_options, but not {validate_text}. Skipping.",
                    )
            if not skip:
                if validate(parsed_opt_value):
                    logger.debug(f"Parsed input from generator_options passed validation")
                    return parsed_opt_value
                else:
                    logger.warn(
                        f"Value was provided in generator_options, but not {validate_text}. Skipping.",
                    )

        while True:
            input_value: str = typer.prompt(
                f"Please enter {input_text} `{variable_name}` ({validate_text})",
            )
            logger.debug(f"Collected input from user: {input_value}")
            try:
                parsed_input_value = parse(input_value)
                logger.debug(f"Parsed input from user: {parsed_input_value}")
                if validate(parsed_input_value):
                    logger.debug(f"Parsed input from user passed validation")
                    return parsed_input_value
                else:
                    logger.error(f"Input must be {validate_text}")
            except ValueError:
                logger.error(f"Input must be {validate_text}")

    def _get_input_name(self, generator_options: str | None) -> str:
        name = self._get_input(
            generator_options,
            "name",
            "the name",
            "a string with length > 0 and < 30",
            str,
            lambda s: len(s) > 0 and len(s) < 30,
        )
        logger.debug(f"Set name to {name}")
        return name

    def _get_input_topology_number_of_nodes(self, generator_options: str | None) -> int:
        number_of_nodes = self._get_input(
            generator_options,
            "number_of_nodes",
            "the number of nodes",
            "a valid integer with value >= 0 and < 100,000",
            int,
            lambda n: n >= 0 and n < 100000,
        )
        logger.debug(f"Set number_of_nodes to {number_of_nodes}")
        return number_of_nodes

    def _get_input_topology_connectivity(
        self,
        generator_options: str | None,
    ) -> Connectivity:
        connectivity = self._get_input(
            generator_options,
            "connectivity",
            "the connectivity",
            "a valid float with value >= 0 and <= 1",
            float,
            lambda n: n >= 0 and n <= 1,
        )
        logger.debug(f"Set connectivity to {connectivity}")
        return connectivity

    @abstractmethod
    def gen(self, generator_options: str | None) -> GeneratorType:
        pass
