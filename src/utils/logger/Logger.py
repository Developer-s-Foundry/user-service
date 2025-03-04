from typing import Any
from logging import getLogger
from collections.abc import Sequence

from src.env import app

from ..svcs import Service
from .LoggerInterface import LoggerInterface


@Service(LoggerInterface)
class Logger:
    def debug(self, message: str, *args: Sequence[Any]) -> None:
        self.__log("debug", message, *args)

    def info(self, message: str, *args: Sequence[Any]) -> None:
        self.__log("info", message, *args)

    def warn(self, message: str, *args: Sequence[Any]) -> None:
        self.__log("warning", message, *args)

    def error(self, message: str, *args: Sequence[Any]) -> None:
        self.__log("error", message, *args)

    def __log(self, level: str, message: str, *args: Sequence[Any]) -> None:
        getLogger().log(level, f"{self.__format_scope} {message}", *args)

    def __format_scope(self) -> str:
        return f"[{app['name']} v{app['version']}]"
