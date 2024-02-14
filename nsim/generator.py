import json
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar
from collections.abc import Callable

import typer

from .util import Json, Connectivity, select, get_file_path_extension
from .input import InputType
from .logger import logger
from .topology.inputs import topology_inputs
from .topology.models.node import Node


TInputType = TypeVar("TInputType")
TGeneratorType = TypeVar("TGeneratorType")


class Generator(Generic[TGeneratorType], metaclass=ABCMeta):
    generator_options: str | None

    def _get_input(
        self,
        variable_name: str,
        input_text: str,
        validate_text: str,
        parse: Callable[[str], TInputType],
        validate: Callable[[TInputType], bool] = lambda _: True,
    ) -> TInputType:
        logger.debug(f"Collecting input for `{variable_name}`")

        if self.generator_options is not None:
            skip = False
            if not skip:
                try:
                    opts: Json = json.loads(self.generator_options)
                    logger.debug("Successfully loaded generator_options")
                except Exception as e:
                    skip = True
                    logger.warn(
                        f"generator_options was provided, but is not valid JSON: {e}. Skipping.",
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
                    logger.debug(
                        f"Parsed input from generator_options: {parsed_opt_value}",
                    )
                except:
                    skip = True
                    logger.warn(
                        f"Value was provided in generator_options, but not {validate_text}. Skipping.",
                    )
            if not skip:
                if validate(parsed_opt_value):
                    logger.debug(
                        f"Parsed input from generator_options passed validation",
                    )
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

    def _get_input_name(self) -> str:
        name = self._get_input(
            "name",
            "the name",
            "a string with length > 0",
            str,
            lambda s: len(s) > 0,
        )
        logger.debug(f"Set name to {name}")
        return name

    def _get_input_number_of_nodes(self) -> int:
        number_of_nodes = self._get_input(
            "number_of_nodes",
            "the number of nodes",
            "a valid integer with value >= 0",
            int,
            lambda n: n >= 0,
        )
        logger.debug(f"Set number_of_nodes to {number_of_nodes}")
        return number_of_nodes

    def _get_input_connectivity(self) -> Connectivity:
        connectivity = self._get_input(
            "connectivity",
            "the connectivity",
            "a valid float with value >= 0 and <= 1",
            float,
            lambda n: n >= 0 and n <= 1,
        )
        logger.debug(f"Set connectivity to {connectivity}")
        return connectivity

    def _get_input_node(self) -> Node:
        def to_node(file_path: str) -> Node:
            i = select(
                "input",
                topology_inputs,
                InputType(get_file_path_extension(file_path)),
            )
            return i.run_super(file_path)

        node = self._get_input(
            "topology",
            "the topology file path",
            "a valid file path including extension",
            to_node,
        )
        logger.debug(f"Set topology to {node}")
        return node

    def _get_input_duration(self) -> float:
        duration = self._get_input(
            "duration",
            "the duration in simulation seconds",
            "a valid float with value >= 0",
            float,
            lambda n: n >= 0,
        )
        logger.debug(f"Set duration to {duration}")
        return duration

    def run_super(self, generator_options: str | None) -> TGeneratorType:
        self.generator_options = generator_options
        result = self.run()
        self.generator_options = None
        return result

    @abstractmethod
    def run(self) -> TGeneratorType:
        pass
