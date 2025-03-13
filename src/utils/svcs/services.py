from typing import TypeVar, get_type_hints

from src.utils.svcs import context

from .registry import svcs_from, get_registry

T = TypeVar("T")


async def Depends(cls: type[T]) -> T:
    request = context.request.get()
    container = svcs_from(request)
    return await container.aget(cls)


class Service:
    def __init__(self, interface: type | None = None) -> None:
        self.interface = interface

    def __call__(self, cls: type[T]) -> type[T]:
        registry = get_registry("api")

        async def factory() -> T:
            """Dynamically resolve dependencies and create an instance."""
            init_params = get_type_hints(cls.__init__)
            dependencies = {}

            for param, param_type in init_params.items():
                if param == "return":
                    continue  # Skip return type

                # Auto-resolve dependencies
                dependencies[param] = await Depends(param_type)

            return cls(**dependencies)

        registry.register_factory(self.interface if self.interface else cls, factory)
        return cls
