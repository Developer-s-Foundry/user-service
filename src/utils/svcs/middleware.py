from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from asgiref.sync import iscoroutinefunction, markcoroutinefunction

from . import context
from .registry import svcs_from


class ContainerMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request: HttpRequest) -> HttpResponse:
        with svcs_from(request):
            context.request.set(request)
            response = await self.get_response(request)
            return response
