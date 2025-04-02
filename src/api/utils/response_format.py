from typing import Any


def success_response(message: str, data: Any = None, status_code: int = 200) -> tuple:  # noqa: ANN401
    return status_code, {"status_code": status_code, "message": message, "data": data}


def error_response(message: str, errors: Any = None, status_code: int = 400) -> tuple:  # noqa: ANN401
    return status_code, {
        "status_code": status_code,
        "message": message,
        "errors": errors,
    }
