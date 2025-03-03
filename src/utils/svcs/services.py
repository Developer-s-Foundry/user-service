from django.http import HttpRequest

from .registry import svcs_from, get_registry


class Service:
    def __init__(self, interface: type | None = None) -> None:
        self.interface = interface

    def __call__(self, cls: type) -> type:
        registry = get_registry("api")
        registry.register_factory(self.interface if self.interface else cls, cls)
        return cls


def Depends(request: HttpRequest, cls: type) -> type:
    container = svcs_from(request)
    return container.aget(cls)
