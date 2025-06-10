from flask import request
from common.exception import ValidationError
import base64


class HeaderGetter:
    @staticmethod
    def _is_not_empty(data):
        if not data:
            return False
        return True

    @staticmethod
    def is_base64(data):
        try:
            base64.b64decode(data, validate=True)
            return True
        except Exception:
            return False

    @classmethod
    def get_x_line_signature(cls):
        x_line_token = request.headers.get("X-Line-Signature")
        if not cls._is_not_empty(x_line_token):
            message = "header could not be empty"
            raise ValidationError(message)
        if not cls.is_base64(x_line_token):
            message = "toke is not base64 encode"
            raise ValidationError(message)
        return x_line_token
