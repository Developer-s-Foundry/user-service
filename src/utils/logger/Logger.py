import logging

from src.env import app

from ..svcs import Service


@Service()
class Logger:
    def debug(
        self, message: str, **kwargs: int | str | list | set | dict | tuple | None
    ) -> None:
        self.__log(logging.DEBUG, message, **kwargs)

    def info(
        self, message: str, **kwargs: int | str | list | set | dict | tuple | None
    ) -> None:
        self.__log(logging.INFO, message, **kwargs)

    def warn(
        self, message: str, **kwargs: int | str | list | set | dict | tuple | None
    ) -> None:
        self.__log(logging.WARNING, message, **kwargs)

    def error(
        self, message: str, **kwargs: int | str | list | set | dict | tuple | None
    ) -> None:
        self.__log(logging.ERROR, message, **kwargs)

    def __log(
        self,
        level: int,
        message: str,
        **kwargs: int | str | list | set | dict | tuple | None,
    ) -> None:
        logging.getLogger().log(
            level,
            f"{self.__format_scope()} {message} {kwargs}",
        )

    def __format_scope(self) -> str:
        return f"[{app['name']} v{app['version']}]"
