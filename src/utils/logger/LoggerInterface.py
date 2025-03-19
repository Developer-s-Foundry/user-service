from typing import Protocol


class LoggerInterface(Protocol):
    def debug(
        self, message: str, **kwargs: int | str | list | set | dict | tuple | None
    ) -> None: ...

    def info(
        self, message: str, **kwargs: int | str | list | set | dict | tuple | None
    ) -> None: ...

    def warn(
        self, message: str, **kwargs: int | str | list | set | dict | tuple | None
    ) -> None: ...

    def error(
        self, message: str, **kwargs: int | str | list | set | dict | tuple | None
    ) -> None: ...
