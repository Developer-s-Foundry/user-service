from typing import TypeVar, Annotated, get_type_hints

from svcs.exceptions import ServiceNotFoundError

from src.utils.logger import Logger

from ..svcs import context
from .registry import svcs_from, get_registry

T = TypeVar("T")


async def ADepends(cls: type[T]) -> T:
    request = context.request.get()
    container = svcs_from(request)
    return await container.aget(cls)


async def get_logger(ann_context: str = "Root") -> Logger:
    ann = Annotated[Logger, ann_context]

    try:
        request = context.request.get()
        container = svcs_from(request)
        return await container.aget(ann)  # type:ignore This was ignored to pass Pyright - it works fine on Mypy
    except ServiceNotFoundError:
        registry = get_registry("api")
        registry.register_factory(ann, lambda: Logger(ann_context))  # type:ignore This was ignored to pass Pyright - it works fine on Mypy
        return await container.aget(ann)  # type:ignore This was ignored to pass Pyright - it works fine on Mypy


class Service:
    def __init__(self, interface: type | None = None) -> None:
        self.interface = interface

    def __call__(self, cls: type[T]) -> type[T]:
        registry = get_registry("api")

        async def factory() -> T:
            """Dynamically resolve dependencies and create an instance."""
            init_params = get_type_hints(cls.__init__, include_extras=True)
            dependencies = {}

            for param, param_type in init_params.items():
                if param == "return":
                    continue  # Skip return type

                if param == "logger":
                    metadata = getattr(param_type, "__metadata__", None)
                    logger_context = metadata[0] if metadata else "Root"
                    dependencies[param] = await get_logger(logger_context)
                else:
                    # Auto-resolve dependencies
                    dependencies[param] = await ADepends(param_type)

            return cls(**dependencies)

        registry.register_factory(self.interface if self.interface else cls, factory)
        return cls
