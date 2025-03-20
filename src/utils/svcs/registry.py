import atexit

import svcs
from django.apps import AppConfig, apps
from django.http import HttpRequest
from asgiref.local import Local

_KEY_CONTAINER = "svcs_container"
_NON_REQUEST_CONTEXT = Local()


def init_registry(app_config: AppConfig) -> None:
    setattr(app_config, "registry", svcs.Registry())


def close_registry(app_config: AppConfig) -> None:
    registry = getattr(app_config, "registry", None)
    if registry:
        atexit.register(registry.close)


def get_registry(
    app_name: str | None = None, app_config: AppConfig | None = None
) -> svcs.Registry:
    if app_name is None and app_config is None:
        raise ValueError("Either app_name or app_config must be provided")
    if app_name:
        config = apps.get_app_config(app_name)
        if not hasattr(config, "registry") or getattr(config, "registry", None) is None:
            raise RuntimeError(f"Registry not initialized for app '{app_name}'")
        return getattr(config, "registry")
    if app_config and (
        hasattr(app_config, "registry")
        and getattr(app_config, "registry", None) is not None
    ):
        return getattr(app_config, "registry")
    raise RuntimeError("Registry not initialized")


def svcs_from(request: HttpRequest | None = None) -> svcs.Container:
    context = request or _NON_REQUEST_CONTEXT
    if not hasattr(context, _KEY_CONTAINER):
        setattr(context, _KEY_CONTAINER, svcs.Container(registry=get_registry("api")))

    return getattr(context, _KEY_CONTAINER)
