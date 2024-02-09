from rich import print
from rich.markup import escape

from .config import LoggingLevel, get_config


class Logger():
    def __should_log(self, allowed_logging_levels: list[LoggingLevel]) -> bool:
        config = get_config()
        return config.logging.level in allowed_logging_levels

    def debug(self, message: str) -> None:
        if self.__should_log([LoggingLevel.DEBUG]):
            print(fr"[bold bright_black]\[Debug][/] {escape(message)}")

    def info(self, message: str) -> None:
        if self.__should_log([LoggingLevel.DEBUG, LoggingLevel.INFO]):
            print(fr"[bold bright_blue]\[Info][/]: {escape(message)}")

    def warn(self, message: str) -> None:
        if self.__should_log([LoggingLevel.DEBUG, LoggingLevel.INFO, LoggingLevel.WARN]):
            print(fr"[bold bright_yellow]\[Warning][/]: {escape(message)}")

    def error(self, message: str) -> None:
        if self.__should_log([LoggingLevel.DEBUG, LoggingLevel.INFO, LoggingLevel.WARN, LoggingLevel.ERROR]):
            print(fr"[bold bright_red]\[Error][/]: {escape(message)}")

logger = Logger()
