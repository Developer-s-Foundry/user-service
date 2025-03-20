from contextvars import ContextVar

request: ContextVar = ContextVar("request", default=None)
