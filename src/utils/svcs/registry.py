import atexit
from typing import Protocol

import svcs
from django.apps import apps
from django.http import HttpRequest
from asgiref.local import Local

_KEY_CONTAINER = "svcs_container"
_NON_REQUEST_CONTEXT = Local()


class DjangoAppConfig(Protocol):
    registry: svcs.Registry


def init_registry(app_config: DjangoAppConfig) -> None:
    app_config.registry = svcs.Registry()


def close_registry(app_config: DjangoAppConfig) -> None:
    atexit.register(app_config.registry.close)


def get_registry(
    app_name: str | None = None, app_config: DjangoAppConfig | None = None
) -> svcs.Registry:
    if app_name is None and app_config is None:
        raise ValueError("Either app_name or app_config must be provided")
    if app_name:
        config = apps.get_app_config(app_name)
        if not hasattr(config, "registry") or config.registry is None:
            raise RuntimeError(f"Registry not initialized for app '{app_name}'")
        return config.registry
    if app_config and (
        hasattr(app_config, "registry") and app_config.registry is not None
    ):
        return app_config.registry
    raise RuntimeError("Registry not initialized")


def svcs_from(request: HttpRequest | None = None) -> svcs.Container:
    context = request or _NON_REQUEST_CONTEXT
    if not hasattr(context, _KEY_CONTAINER):
        setattr(context, _KEY_CONTAINER, svcs.Container(registry=get_registry("api")))

    return getattr(context, _KEY_CONTAINER)
