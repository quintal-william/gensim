import json
from dataclasses import dataclass
from enum import Enum
from typing import Annotated

import typer


class LoggingLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"

def set_config(logging_level: LoggingLevel) -> None:
    global config
    config = Config( # type: ignore [name-defined]
        logging=LoggingConfig(
            level=logging_level,
        ),
    )

def set_logging_level(logging_level: LoggingLevel) -> None:
    set_config(logging_level=logging_level)

LoggingLevelOption = Annotated[
    LoggingLevel, typer.Option(
        help="Set the granularity with which logs will be printed to the console",
        rich_help_panel="Config",
        callback=set_logging_level,
    ),
]

LoggingLevelDefault = LoggingLevel.INFO

@dataclass
class LoggingConfig:
    level: LoggingLevel

@dataclass
class Config:
    logging: LoggingConfig

    def to_json(self) -> str:
        config_dict = {
            "logging": {
                "level": self.logging.level,
            },
        }
        return json.dumps(config_dict)

def get_config() -> Config:
    try:
        global config
        return config # type: ignore
    except NameError:
        raise RuntimeError("Please use set_config before using get_config")
