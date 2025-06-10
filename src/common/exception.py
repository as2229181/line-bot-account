from common import error_code
from common.error_code import ErrorCode


def make_error_schema(message, error_code, error_key):
    _dict = {
        "message": message,
        "error_code": error_code,
        "error_key": error_key,
    }
    return _dict


class _BaseError(Exception):
    def __init__(self, code=404, message=None, error_code=None, debug_message=None):
        self.code = code
        self.message = message
        self.error_code = error_code or ErrorCode.BASE_ERROR
        self.debug_message = debug_message

    def __str__(self):
        return f"{self.message}\n >>> .debug: {self.debug_message}"

    def __repr__(self):
        lines = list()

        for k, v in self.__dict__.items():
            lines.append(f"{k}={v}")

        args_line = ", ".join(lines)
        text = f"{self.__class__.__name__}({args_line})"
        return text

    def to_dict(self):
        _schema = make_error_schema(
            message=self.message,
            error_code=self.error_code,
            error_key=self.error_code,
        )
        return _schema


class ValidationError(_BaseError):
    def __init__(self, message=None, error_code=None, debug_message=None):
        super().__init__(
            code=400,
            message=message or "Validation Error",
            error_code=error_code or ErrorCode.BASE_ERROR,
            debug_message=debug_message,
        )


class ExternalError(_BaseError):
    def __init__(self, message=None, error_code=None, debug_message=None):
        super().__init__(
            code=400,
            message=message or "External Service Error",
            error_code=error_code or ErrorCode.SERVICE_ERROR,
            debug_message=debug_message,
        )
